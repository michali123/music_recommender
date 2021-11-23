from flask import Flask
from flask import render_template, request, jsonify, url_for, redirect, session
import requests
import json
import time
import atexit
from apscheduler.schedulers.background import BackgroundScheduler
from flask_apscheduler import APScheduler
from Pulsoid import *
from config import *
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from config import CLIENT_ID, CLIENT_SECRET
from json2html import *

app = Flask(__name__)

app.secret_key = "rfgt535"
# app.config[SESSION_COOKIE_NAME]='Michal'


@app.route("/")  # goes to main page
def index():
    tokenData = getPulsoidToken()
    print(tokenData['scopes'][0])
    heartRate = getPulsoidHR()
    access_token = getTokenInfo()
    if access_token:
        print("Access token available! Trying to get user information...")
        sp = spotipy.Spotify(access_token)
        user = sp.current_user()
        print(json.dumps(user, sort_keys=True, indent=4))
    return render_template("index.html", hr=heartRate, checkPulsoid=getPulsoidConnecetionStatus())


@app.route('/login')
def login():
    sp_oauth = create_spotify_oauth()
    auth_url = sp_oauth.get_authorize_url()
    print("authUrl", auth_url)
    return redirect(auth_url)


def getTokenInfo():
    sp_oauth = create_spotify_oauth()
    session.clear()
    code = request.args.get('code')
    token_info = sp_oauth.get_access_token(code)
    access_token = token_info["access_token"]
    print("TOKEN INFO IS:", token_info)
    session["token_info"] = token_info
    # Checking if token has expired
    now = int(time.time())
    is_token_expired = session.get('token_info').get('expires_at') - now < 60

    # Refreshing token if it has expired
    if (is_token_expired):
        sp_oauth = create_spotify_oauth()
        token_info = sp_oauth.refresh_access_token(
            session.get('token_info').get('refresh_token'))
    return access_token


@app.route('/playlistRecommender', methods=['GET', 'POST'])
def playlistRecommender():
    access_token = getTokenInfo()
    if access_token:
        print("Access token available! Trying to get user information...")
        sp = spotipy.Spotify(access_token)
        user = sp.current_user()
        user_id = user["id"]
        # print(json.dumps(user, sort_keys=True, indent=4))
        # tracks = [Track(track["track"]["name"], track["track"]["id"], track["track"]["artists"][0]["name"]
        jsonTracks = sp.current_user_recently_played()
        recommended_tracks = sp.recommendations(limit=5, seed_artists=["4NHQUGzhtTLFvgF5SZesLK"], seed_genres=[
                                                "country"], seed_tracks=["0c6xIDDpzE81m2q797ordA"])
        tracks_id = []

        for i in recommended_tracks['tracks']:
            track_id = i['id']
            tracks_id.append(track_id)
            # print(track_id)

        init_playlist = sp.user_playlist_create(
            user_id, "NextSong", public=True, collaborative=False, description='Your curated ML music recommender! by NextSong')
        playlist_embed_link = init_playlist["external_urls"]["spotify"]
        user_playlist_id = init_playlist["id"]
        creating_playlist = sp.user_playlist_add_tracks(
            user_id, user_playlist_id, tracks_id, position=None)
        test = recommended_tracks
        # return jsonify(playlist) #jsonify lets us return a list
        return render_template("spotifyRecommender.html", playlist_embed_link=playlist_embed_link)
# jsonfile=json.dumps(jsonTracks)


def create_spotify_oauth():
    return SpotifyOAuth(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        redirect_uri=url_for('playlistRecommender', _external=True),
        scope="user-top-read user-read-recently-played user-library-read user-read-currently-playing playlist-read-collaborative playlist-read-private playlist-modify-public user-modify-playback-state user-read-playback-state")


@app.route('/artist/<id>')
def artist(id):
    artist = spotify.get_artist(id)
    if artist['images']:
        image_url = artist['images'][0]['url']
    else:
        image_url = 'http://placecage.com/600/400'

    tracksdata = spotify.get_artist_top_tracks(id)
    tracks = tracksdata['tracks']

    artistsdata = spotify.get_related_artists(id)

    audio_features = []

    for i in range(9):
        for k, v in tracks[i].items():
            if k == "id":
                audio_features.append(search_audio_features(v))

    predictions_list = []
    regr(audio_features, predictions_list)

    tokenData = getPulsoidToken()
    heartRate = getPulsoidHR()

    relartists = artistsdata['artists']
    html = render_template('index.html',
                           hr=heartRate,
                           checkSpotify=get_spotify_connnection_stauts(),
                           checkPulsoid=getPulsoidConnecetionStatus(),
                           artist=artist,
                           related_artists=relartists,
                           image_url=image_url,
                           tracks=tracks,
                           predictions_list=predictions_list)
    return html


@app.route('/name', methods=["POST"])
def namee():
    result = request.form["fname"]
    data = spotify.search_by_artist_name(result)
    api_url = data['artists']['href']
    items = data['artists']['items']
    print(items[0])
    tokenData = getPulsoidToken()
    heartRate = getPulsoidHR()

    html = render_template('index.html', hr=heartRate,
                           checkSpotify=get_spotify_connnection_stauts(),
                           checkPulsoid=getPulsoidConnecetionStatus(), results=items)

    return html


if __name__ == "__main__":
    app.run(debug=True)

# Shut down the scheduler when exiting the app
# atexit.register(lambda: scheduler.shutdown())

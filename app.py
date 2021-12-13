from flask import Flask
from flask import render_template, request, jsonify,url_for, redirect, session
import requests, json
import time
import atexit
from apscheduler.schedulers.background import BackgroundScheduler
from flask_apscheduler import APScheduler
from spotify import *
from Pulsoid import *
from config import *
import spotify
import spotipy
from algorithm import regr
from spotipy.oauth2 import SpotifyOAuth
from config import CLIENT_ID, CLIENT_SECRET
from json2html import *
import threading
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy.util as util
import pandas as pd
from musicnn.tagger import top_tags
from tempocnn.classifier import TempoClassifier
from tempocnn.feature import read_features

import os

# from secrets import PULSOID_SECRET_KEY

app = Flask(__name__)

app.secret_key = "rfgt535"
# app.config[SESSION_COOKIE_NAME]='Michal'

@app.route("/")  # goes to main page
def index():
    tokenData = getPulsoidToken()
    print(tokenData['scopes'][0])
    getPulsoidHR()  
    heartRate = getPulsoidHR()
    access_token = getTokenInfo()
    if access_token:
        print("Access token available! Trying to get user information...")
        sp = spotipy.Spotify(access_token)
        user = sp.current_user()
        print(json.dumps(user, sort_keys=True, indent=4))
    return render_template("record.html", hr=heartRate, checkPulsoid=getPulsoidConnecetionStatus())

@app.route('/login')
def login():
    sp_oauth = create_spotify_oauth()
    auth_url = sp_oauth.get_authorize_url()
    return redirect(auth_url)




def getTokenInfo():
    sp_oauth = create_spotify_oauth()
    session.clear()
    code = request.args.get('code')
    token_info = sp_oauth.get_access_token(code)
    access_token = token_info["access_token"]
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


if __name__ == "__main__":

    app.run(debug=True)

# Shut down the scheduler when exiting the app
# atexit.register(lambda: scheduler.shutdown())


    
@app.route('/artist/<id>', methods=['GET', 'POST'])
def artist(id):


    artist = spotify.get_artist(id)
    if artist['images']:
        image_url = artist['images'][0]['url']
    else:
        image_url = 'http://placecage.com/600/400'

    tracksdata = spotify.get_artist_top_tracks(id)
    tracks = tracksdata['tracks']

    artistsdata = spotify.get_related_artists(id)

    audio_features=[]

    for i in range(10):
      for k,v in tracks[i].items():
          if k == "id":
                audio_features.append(search_audio_features(v))

    predictions_list = []
    predicted_tags = []
    regr(audio_features, predictions_list)

    #final_df = compare_features(audio_features)
    

    tokenData = getPulsoidToken()
    heartRate = getPulsoidHR()
    
    relartists = artistsdata['artists']

    # predict heart - rate 
    model_name = 'cnn'
    if len(os.listdir(r"C:\Users\abelf\Downloads\music_recommender\audio downloaded")) > 0:

        music = os.listdir(r"C:\Users\abelf\Downloads\music_recommender\audio downloaded")[-1]
        path_folder = "C:\\Users\\abelf\\Downloads\\music_recommender\\audio downloaded"+ "\\" + music

        # initialize the model (may be re-used for multiple files)
        classifier = TempoClassifier(model_name)

        # read the file's features
        features = read_features(path_folder)

        # estimate the global tempo
        tempo = classifier.estimate_tempo(features, interpolate=False)



    # predict tags 
    if len(os.listdir(r"C:\Users\abelf\Downloads\music_recommender\audio downloaded")) > 0:
        music = os.listdir(r"C:\Users\abelf\Downloads\music_recommender\audio downloaded")[-1]
        path_folder = "C:\\Users\\abelf\\Downloads\\music_recommender\\audio downloaded"+ "\\" + music

        os.rename(path_folder,path_folder.strip(".wav") + ".mp3")
        music = os.listdir(r"C:\Users\abelf\Downloads\music_recommender\audio downloaded")[-1]
        path_folder = "C:\\Users\\abelf\\Downloads\\music_recommender\\audio downloaded"+ "\\" + music

        predicted_tags= top_tags(path_folder, model='MTT_musicnn', topN=3)
        os.remove(path_folder)

   
    if len(predicted_tags)>0: 
        html = render_template('record.html',
                                hr = heartRate,
                                checkSpotify=get_spotify_connnection_stauts(),
                                checkPulsoid=getPulsoidConnecetionStatus(),
                                artist=artist,
                                related_artists=relartists,
                                image_url=image_url,
                                tracks=tracks,
                                predictions_list = predictions_list, 
                                predicted_tags = predicted_tags,
                                tempo = tempo)
    else:
        html = render_template('record.html',
                                hr = heartRate,
                                checkSpotify=get_spotify_connnection_stauts(),
                                checkPulsoid=getPulsoidConnecetionStatus(),
                                artist=artist,
                                related_artists=relartists,
                                image_url=image_url,
                                tracks=tracks,
                                predictions_list = predictions_list, 
                                )

    return html









# custom playlist based on artist search
@app.route('/playlistRecommender-artist', methods=['GET', 'POST'])
def playlistRecommenderforartist():
    user_name = request.form["fplaylist"]
    access_token = getTokenInfo()
    print("I am in")
    if access_token:

        artist_name = spotify.search_by_artist_name_to_get_id(user_name)
        print("Access token available! Trying to get user information...")
        sp = spotipy.Spotify(access_token)
        user = sp.current_user()
        user_id = user["id"]
        # print(json.dumps(user, sort_keys=True, indent=4))
        # tracks = [Track(track["track"]["name"], track["track"]["id"], track["track"]["artists"][0]["name"]
        jsonTracks = sp.current_user_recently_played()
        recommended_tracks = sp.recommendations(limit=30,seed_artists=[artist_name], seed_genres=["country"])
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









# Shut down the scheduler when exiting the app
# atexit.register(lambda: scheduler.shutdown())






@app.route('/name', methods = ["POST"])
def namee():
    result = request.form["fname"]
    data = spotify.search_by_artist_name(result)
    api_url = data['artists']['href']
    items = data['artists']['items']
    tokenData = getPulsoidToken()
    heartRate = getPulsoidHR()


    html = render_template('record.html',hr = heartRate,
                            checkSpotify=get_spotify_connnection_stauts(),
                            checkPulsoid=getPulsoidConnecetionStatus(),results=items)

    
    return html




if __name__== "__main__":
    app.run(debug=True)

# Shut down the scheduler when exiting the app
# atexit.register(lambda: scheduler.shutdown())

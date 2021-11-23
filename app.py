from flask import Flask
from flask import render_template, request, jsonify
import requests, json
import time
import atexit
from apscheduler.schedulers.background import BackgroundScheduler
from flask_apscheduler import APScheduler
from spotify import *
from Pulsoid import *
from config import *
import spotify
from algorithm import regr


# from secrets import PULSOID_SECRET_KEY

app = Flask(__name__)

check = get_spotify_connnection_stauts()
getPulsoidConnecetionStatus()


scheduler = BackgroundScheduler()
scheduler.add_job(func=getPulsoidHR, trigger="interval", seconds=3)
# scheduler.start()

@app.route("/") #goes to main page
def index():
    tokenData = getPulsoidToken()
    print(tokenData['scopes'][0])
    heartRate = getPulsoidHR()

    return render_template("index.html", hr= heartRate,checkSpotify=get_spotify_connnection_stauts(),
    checkPulsoid=getPulsoidConnecetionStatus() )



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

    audio_features=[]

    for i in range(9):
      for k,v in tracks[i].items():
          if k == "id":
                audio_features.append(search_audio_features(v))

    predictions_list = []
    regr(audio_features, predictions_list)


    tokenData = getPulsoidToken()
    heartRate = getPulsoidHR()
    
    relartists = artistsdata['artists']
    html = render_template('index.html',
                            hr = heartRate,
                            checkSpotify=get_spotify_connnection_stauts(),
                            checkPulsoid=getPulsoidConnecetionStatus(),
                            artist=artist,
                            related_artists=relartists,
                            image_url=image_url,
                            tracks=tracks,
                            predictions_list = predictions_list)
    return html

@app.route('/name', methods = ["POST"])
def namee():
    result = request.form["fname"]
    data = spotify.search_by_artist_name(result)
    api_url = data['artists']['href']
    items = data['artists']['items']
    print(items[0])
    tokenData = getPulsoidToken()
    heartRate = getPulsoidHR()


    html = render_template('index.html',hr = heartRate,
                            checkSpotify=get_spotify_connnection_stauts(),
                            checkPulsoid=getPulsoidConnecetionStatus(),results=items)

    
    return html






if __name__== "__main__":
    app.run(debug=True)

# Shut down the scheduler when exiting the app
# atexit.register(lambda: scheduler.shutdown())

from flask import Flask
from flask import render_template, request, jsonify
import requests, json
import time
import atexit
from apscheduler.schedulers.background import BackgroundScheduler
from flask_apscheduler import APScheduler
from spotify import *
from Pulsoid import *
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


if __name__== "__main__":
    app.run(debug=True)

# Shut down the scheduler when exiting the app
# atexit.register(lambda: scheduler.shutdown())

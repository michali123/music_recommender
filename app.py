from flask import Flask
from flask import render_template, request, jsonify
import requests, json
import time
import atexit
from apscheduler.schedulers.background import BackgroundScheduler
from flask_apscheduler import APScheduler
# from secrets import PULSOID_SECRET_KEY

app = Flask(__name__)

def getPulsoidToken():
    headers = {
    'Authorization': 'Bearer 52fb90c7-0c50-4927-89a3-db12802ee857',
    'Content-Type': 'application/json',
    }
    response = requests.get('https://dev.pulsoid.net/api/v1/token/validate', headers=headers)
    tokenData = response.json()
    return tokenData

def getPulsoidHR():
    headers = {
        'Authorization': 'Bearer 52fb90c7-0c50-4927-89a3-db12802ee857',
        'Content-Type': 'application/json',
    }
    response = requests.get('https://dev.pulsoid.net/api/v1/data/heart_rate/latest', headers=headers)
    heartRate = response.json()
    print("Current heart rate:" , heartRate['data']['heart_rate'])
    heartRate = heartRate['data']['heart_rate']
    return heartRate

scheduler = BackgroundScheduler()
scheduler.add_job(func=getPulsoidHR, trigger="interval", seconds=3)
# scheduler.start()
@app.route("/") #goes to main page
def index():
    tokenData = getPulsoidToken()
    print(tokenData['scopes'][0])
    heartRate = getPulsoidHR()

    return render_template("index.html", hr= heartRate)


if __name__== "__main__":
    app.run(debug=True)

# Shut down the scheduler when exiting the app
# atexit.register(lambda: scheduler.shutdown())

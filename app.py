from flask import Flask
from flask import render_template, request
import requests, json
import time
import atexit
from apscheduler.schedulers.background import BackgroundScheduler
from flask_apscheduler import APScheduler
# from secrets import PULSOID_SECRET_KEY

# set configuration values
class Config:
    SCHEDULER_API_ENABLED = True


app = Flask(__name__)


@app.route("/") #goes to main page
def index():
    tokenData = getPulsoidToken()
    heartRate = getPulsoidHR()
    print(tokenData['scopes'][0])
    print("Current heart rate:" , heartRate['data']['heart_rate'])
    renewAPIcall(getPulsoidHR)
    return render_template("index.html", hr= heartRate['data']['heart_rate'])



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
    return heartRate

def renewAPIcall(gettingHRfunc):
    print("current time taken" , time.strftime("%A, %d. %B %Y %I:%M:%S %p"))
    scheduler = BackgroundScheduler()
    scheduler.add_job(func=gettingHRfunc, trigger="interval", seconds=1)
    scheduler.start()
    # Shut down the scheduler when exiting the app
    atexit.register(lambda: scheduler.shutdown())


if __name__== "__main__":
    app.run(debug=True)

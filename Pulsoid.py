from flask import Flask
from flask import render_template, request, jsonify
import requests, json


def getPulsoidToken():
    headers = {
    'Authorization': 'Bearer 52fb90c7-0c50-4927-89a3-db12802ee857',
    'Content-Type': 'application/json',
    }
    response = requests.get('https://dev.pulsoid.net/api/v1/token/validate', headers=headers)
    tokenData = response.json()
    err_substring = "error_code"
    if err_substring in tokenData:
        print("Oops! token hasn't been received",tokenData)
    return tokenData

def getPulsoidConnecetionStatus():
    tokenData = getPulsoidToken()
    err_substring = "error_code"
    if err_substring in tokenData:
        return False
    return True


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

import requests
import streamlit as st

def readAll():
    response = requests.get("https://atsnet.fastgenapp.com/readAll")
    return response.json()

def holdDB(id):
    headers = {'Content-Type': 'application/json'}
    json_data = {
        'id': id,
        'hold': 'Hold',
    }
    response = requests.post("https://atsnet.fastgenapp.com/holdDB", headers=headers, json=json_data)

def resetDB(id):
    headers = {'Content-Type': 'application/json'}
    json_data = {
        'id': id,
        'reset': 'Reset',
    }
    response = requests.post("https://atsnet.fastgenapp.com/resetDB", headers=headers, json=json_data)  

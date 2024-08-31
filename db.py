import requests
import streamlit as st

def readAll():
    response = requests.get(st.secrets["readall"])
    return response.json()

def holdDB(id):
    headers = {'Content-Type': 'application/json'}
    json_data = {
        'id': id,
        'hold': 'Hold',
    }
    response = requests.post(st.secrets["holddb"], headers=headers, json=json_data)

def resetDB(id):
    headers = {'Content-Type': 'application/json'}
    json_data = {
        'id': id,
        'reset': 'Reset',
    }
    response = requests.post(st.secrets["resetdb"], headers=headers, json=json_data) 

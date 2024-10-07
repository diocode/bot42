import os
import time
from oauthlib.oauth2 import BackendApplicationClient
from requests_oauthlib import OAuth2Session
from requests.auth import HTTPBasicAuth
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from pprint import pprint
import requests
import json

# 42 API authentication
def get_42_api_token():
    client_id = os.getenv("INTRA_UID")
    client_secret = os.getenv("INTRA_SECRET")
    token_url = 'https://api.intra.42.fr/oauth/token'
    
    data = {
        'grant_type': 'client_credentials',
        'client_id': client_id,
        'client_secret': client_secret
    }
    
    response = requests.request('POST', token_url, data=data)
    if response.status_code == 200:
        return response.json()['access_token']
    else:
        raise Exception("Failed to obtain 42 API token")

# Initialize Slack app
try:
    app = App(token=os.environ["SLACK_BOT_TOKEN"])
except KeyError:
    raise Exception("SLACK_BOT_TOKEN environment variable not set")

def validate_student(user):
    token = get_42_api_token()
    url = f"https://api.intra.42.fr/v2/users/{user}"
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(url, headers=headers)
    return response.status_code == 200

@app.message("")
def student_grades(message, say):
    if message["text"].lower().startswith("_student"):
        try:
            user = message["text"].split(" ")[1]
            if validate_student(user):
                say("LOOKING FOR STUDENT GRADES...", thread_ts=message["ts"])
            else:
                say("Invalid student", thread_ts=message["ts"])
        except IndexError:
            say("Invalid command format. Use '_student <username>'", thread_ts=message["ts"])

def main():
    try:
        handler = SocketModeHandler(app, os.environ["SLACK_APP_TOKEN"])
        handler.start()
    except KeyError:
        raise Exception("SLACK_APP_TOKEN environment variable not set")

if __name__ == "__main__":
    main()

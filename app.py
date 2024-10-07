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

client_id='INTRA_UID'
client_secret='INTRA_SECRET'

auth = HTTPBasicAuth(client_id, client_secret)
client = BackendApplicationClient(client_id=client_id)
oauth = OAuth2Session(client=client)
token = oauth.fetch_token(token_url='https://api.intra.42.fr/oauth/token', auth=auth)

app = App(token=os.environ.get("SLACK_BOT_TOKEN"))

def refresh_token_if_expired():
    if token.get('expires_at') and token['expires_at'] <= time.time():
        new_token = oauth.refresh_token(token_url='https://api.intra.42.fr/oauth/token')
        token.update(new_token)

def validateStudent(message, say):
    if message["text"].lower().startswith("_student"):
        try:
            user = message["text"].split(" ")[1]
            url = f"https://api.intra.42.fr/v2/users/{user}"
            
            # Refresh token if needed
            refresh_token_if_expired()
            
            # Use the OAuth2Session to make the request
            response = oauth.get(url)
            
            if response.status_code == 200:
                return True
            else:
                raise ValueError
        except (IndexError, ValueError) as e:
            say("Invalid student", thread_ts=message["ts"])
            return False

@app.message("")
def	studentGrades(message, say):
	if not validateStudent(message, say):
		return
	say("LOOKING FOR STUDENT GRADES...", thread_ts=message["ts"])


def main():
    SocketModeHandler(app, os.environ["SLACK_APP_TOKEN"]).start()

if __name__ == "__main__":
    main()

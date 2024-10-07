import os
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

def getAcessToken():
	url = "https://api.intra.42.fr/oauth/token"

	payload = json.dumps({
	"grant_type": "client_credentials",
	"client_id": "",
	"client_secret": ""
	})
	headers = {
	'Content-Type': 'application/json',
	'Cookie': '_mkra_stck=15e20a8020c702e70007eb1e185a06fb%3A1728048352.5550666'
	}

	response = requests.request("POST", url, headers=headers, data=payload)
	response_json = response.json()
	access_token = response_json.get("access_token")

	return access_token

@app.message()
def validateStudent(message, say):
	if message["text"].lower() == "student":
		say(f"<@{message['user']}>") #just to make sure the bot is working
		url = "https://api.intra.42.fr/v2/users/digoncal"
		payload = {}
		headers = {'Authorization': 'Bearer ' + getAcessToken()}
		response = requests.request("GET", url, headers=headers, data=payload)
		print(response.text)

def main():
    SocketModeHandler(app, os.environ["SLACK_APP_TOKEN"]).start()

if __name__ == "__main__":
    main()

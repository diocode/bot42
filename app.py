import os
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from pprint import pprint
from requests_oauthlib import OAuth1Session
import requests
import json

intra = OAuth1Session('client_key',
    client_secret='client_secret',
    resource_owner_key='INTRA_UID',
    resource_owner_secret='INTRA_SECRET'
)
request_token = 'https://api.intra.42.fr/oauth/token'
r = intra.post(request_token)

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

if __name__ == "__main__":
    SocketModeHandler(app, os.environ["SLACK_APP_TOKEN"]).start()

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
	"client_id": "u-s4t2af-32b987953f9d75fe9901c49b8cc80a32da7dddf93afe4a2cca080efedf917e30",
	"client_secret": "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"
	})
	headers = {
	'Content-Type': 'application/json',
	'Cookie': '_mkra_stck=15e20a8020c702e70007eb1e185a06fb%3A1728048352.5550666'
	}

	response = requests.request("POST", url, headers=headers, data=payload)
	response_json = response.json()
	access_token = response_json.get("access_token")

	return access_token

@app.message("")
def validateStudent(message, say):
	if message["text"].lower().startswith("_student"):
		user = message["text"].split(" ")[1]

		url = "https://api.intra.42.fr/v2/users/" + user
		payload = {}
		headers = {'Authorization': 'Bearer ' + getAcessToken()}
		response = requests.request("GET", url, headers=headers, data=payload)
		
		if response.status_code == 200:
			say("User " + user + " exists")
		else:
			say("User " + user + " does not exist")

if __name__ == "__main__":
    SocketModeHandler(app, os.environ["SLACK_APP_TOKEN"]).start()

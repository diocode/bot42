import os
import time
from oauthlib.oauth2 import BackendApplicationClient
from requests_oauthlib import OAuth2Session
from requests.auth import HTTPBasicAuth
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from pprint import pprint
from pprint import pformat
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
    response = requests.request('GET', url, headers=headers)
    return response.status_code == 200

# Get all projects
def get_all_projects():
    token = get_42_api_token()
    url = "https://api.intra.42.fr/v2/projects"
    headers = {"Authorization": f"Bearer {token}"}
    
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        raise Exception("Failed to retrieve projects: " + response.text)

    pprint(response.json())
    return response.json()

def get_project_id(project_name):
    try:
        projects = get_all_projects()
        project_id = None

        for project in projects:
            if project['name'] == project_name:
                project_id = project['id']
                break

        if project_id:
            return project_id
        else:
            print(f"Project '{project_name}' not found.")
            return 0
    except Exception as e:
        print(f"Error: {e}")

def project_users(project_name):
    token = get_42_api_token()
    cursus_id = get_project_id(project_name)
    url = f"https://api.intra.42.fr/v2/cursus/{cursus_id}/users"
    headers = {"Authorization": f"Bearer {token}"}
    
    response = requests.request('GET', url, headers=headers)
    
    if response.status_code != 200:
        raise Exception("Failed to retrieve users: " + response.text)

    users = response.json()
    completed_users = []

    for user in users:
        if 'projects_users' in user:
            for project in user['projects_users']:
                if project.get('project', {}).get('name') == project_name and project.get('status') == 'finished':
                    completed_users.append(user['login'])

    return completed_users

@app.message("")
def student_grades(message, say):
    if message["text"].lower().startswith("_student"): #handle message: _student *
        try:
            user = message["text"].split(" ")[1]
            if validate_student(user):
                say("Valid student", thread_ts=message["ts"])
            else:
                say("Invalid student", thread_ts=message["ts"])
        except IndexError:
            say("Invalid command format. Use '_student <username>'", thread_ts=message["ts"])

    if message["text"].lower().startswith("_project"): #handle message: _project *
        try:
            completed_users = project_users('C Piscine C 02')
            if completed_users:
                say("Users who finished exam00:\n" + "\n".join(completed_users), thread_ts=message["ts"])
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
# LINKS

## Usage

```sh
python3 -m venv .venv

source .venv/bin/activate
source .env

pip install -r requirements.txt

python3 app.py
```

## Python Docs

https://docs.python.org/3/library/venv.html

## Slack Bolt API

https://api.slack.com/apps
<br/>
https://tools.slack.dev/bolt-python/getting-started
<br/>
https://pypi.org/project/slack-bolt/
<br/>
https://api.slack.com/methods

## API KEYS

- Go to https://api.slack.com/apps/ and get App Level Token

- Go to OAuth & Permissions and get Bot Token

## Tools

- https://httpie.io/docs/cli

## POSTMAN

GET working:
- Create a [POST: {{base_url}}/oauth/token] using your client ID and secret to get your access token from the 42API;
- Create a [GET: {{base_url}}/v2/users/{{id}}] and add in the 'token' field access token from the previous step;

(check the screenshot for reference)

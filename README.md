# LINKS

## Usage

```sh
./build.sh

source .env

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

## OAUTH for Python

https://github.com/requests/requests-oauthlib

## Tools

- https://httpie.io/docs/cli


## POSTMAN
        
- Create a [POST: {{base_url}}/oauth/token] using your client ID and secret to get your access token from the 42API;
- Create a [GET: {{base_url}}/v2/users/{{id}}] and add in the 'token' field access token from the previous step;

Note: After doing this sucessully, go to the bar on the rignt in postman and there's a </> icon that turns the request into python code.
<br/>
(check the screenshot for reference)
![Screenshot from 2024-10-03 16-36-11](https://github.com/user-attachments/assets/f58467d2-6738-4649-8b11-70bff729b596)
![Screenshot from 2024-10-03 16-36-57](https://github.com/user-attachments/assets/a6457bd0-c346-4e90-a2d3-918a03afb229)


### BOT Features

- Search For Pisciner's Progress
- Get General Project Stats
- Get Exam Results


# TODO

- Search student by computer ID
- Warning in case of Project & Exam mismatch
- Print warnings List

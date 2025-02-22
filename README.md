![banners-17](https://github.com/user-attachments/assets/f3a2b8d7-acb7-4093-bf7c-35232874ed7c)

<p align="center">
	<a href="#about">About</a> •
	<a href="#how-to-use">How to use</a> •
	<a href="#api-keys">API Keys</a> •
	<a href="#tools">Tools</a>
</p>

## ABOUT

This project is a Slack bot designed to interact with the 42API, helping users fetch relevant student data efficiently. Using Python, Slack Bolt API, and OAuth authentication, this bot can search for students, retrieve project stats, locate users, and check exam results. 🚀

The bot is configured with environment variables for authentication and leverages Python’s virtual environments for dependency management. Below, you'll find setup instructions, API key retrieval steps, and useful tools for debugging and testing requests.

<br>

### BOT FEATURES

- 🔍 Search for Pisciner's Progress
- 📊 Get general project stats of a student: `_student <username>`
- 🔎 Search student by computer ID: `_locate <computer_id>`
- 🖥️ Search computer by user ID: `_locate <user_ID>`
- 🏆 Get Piscine users and exam results: `_piscine <campus> <year> <month>`
- 📊 Evaluates if any pisciner needs help (care) or has given up (warn):

  `_piscine <campus> <year> <month> <warn/care>`

<br>

## HOW TO USE
### COMPILATION AND EXECUTION
#### 1º - Clone the repository
```bash
$ ./git clone git@github.com:diocode/slack_manager_bot.git
```

#### 2º - Create a .env file and set your credentials
```bash
export SLACK_BOT_TOKEN="your_token"
export SLACK_APP_TOKEN="your_token"
export INTRA_UID="your_token"
export INTRA_SECRET="your_token"
```

### 3º - Build and activate the virtual environment
```bash
$ ./build.sh
$ source .venv/bin/activate
$ source .env
```

### 4º - Run the bot
```bash
$ source .venv/bin/activate
```

### 5º - Clean up the virtual environment
```bash
$ make clean
```

<br>

## API KEYS
- Visit [Slack API Apps](https://api.slack.com/apps/) and create an App-Level Token
- Navigate to OAuth & Permissions and get your Bot Token

- To get the 42 API tokens you need to login into your 42 account and navigate to Settings > API

<br>

## TOOLS
- [Python Virtual Environments](https://docs.python.org/3/library/venv.html)
- [Slack Bolt API](https://tools.slack.dev/bolt-python/getting-started)
- [Slack-Bolt pypi](https://pypi.org/project/slack-bolt/)
- [OAuth for Python](https://github.com/requests/requests-oauthlib)
- [HTTPie CLI](https://httpie.io/docs/cli)
- [Postman](https://www.postman.com/)

### Postman
> You can use **postman** to check if the keys/tokens and requests are working as intended

- Create a `POST: {{base_url}}/oauth/token` using your client ID and secret to get your access token from the 42API;
- Create a `GET: {{base_url}}/v2/users/{{id}}` and add in the 'token' field access token from the previous step;

<br>

After doing this successfully, go to the bar on the rignt in postman and there's a **</>** icon that turns the request into python code.
<br>
*(check the screenshot for reference)*

![373320875-f58467d2-6738-4649-8b11-70bff729b596](https://github.com/user-attachments/assets/4c381464-784b-40f3-8869-e81914018b0b)

![373320917-a6457bd0-c346-4e90-a2d3-918a03afb229](https://github.com/user-attachments/assets/2d7b7e62-24e3-433a-8259-e9c4fd84b8dc)

<br>

This bot simplifies searching for 42 students and their progress through Slack, integrating seamlessly with the 42API


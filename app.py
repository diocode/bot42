import os
from slack_bolt.adapter.socket_mode import SocketModeHandler
import app.slack_bot as slack_bot

def main():
    try:
        handler = SocketModeHandler(slack_bot.app, os.environ["SLACK_APP_TOKEN"])
        handler.start()
    except KeyError:
        raise Exception("SLACK_APP_TOKEN environment variable not set")

if __name__ == "__main__":
    main()

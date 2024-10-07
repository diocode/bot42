import os
from slack_bolt.adapter.socket_mode import SocketModeHandler
from app.slack_bot import app

def main():
    try:
        handler = SocketModeHandler(app, os.environ["SLACK_APP_TOKEN"])
        handler.start()
    except KeyError:
        raise Exception("SLACK_APP_TOKEN environment variable not set")

if __name__ == "__main__":
    main()

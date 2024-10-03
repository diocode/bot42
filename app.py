import os
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from pprint import pprint

app = App(token=os.environ.get("SLACK_BOT_TOKEN"))

@app.message()
def sendMessage(message, say, client):
	#pprint(message)
	if message["text"] == "hello":
		say(f"Hey there <@{message['user']}>!")

	if message["text"] == ":gandalf:":
		say(text="There you go again Pedro! :gandalf:", thread_ts=message["ts"])
	
		client.reactions_add(
			channel=message["channel"],
			name="gandalf",
			timestamp=message["event_ts"]
		)

@app.event("reaction_added")
def sendReaction(event, say, client):
	#pprint(event)
	if event["reaction"] == "gandalf":
		say(text="There you go again Pedro! :gandalf:", thread_ts=event["item"]["ts"])
	

if __name__ == "__main__":
    SocketModeHandler(app, os.environ["SLACK_APP_TOKEN"]).start()

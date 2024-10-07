import os
from slack_bolt import App
from .api import get_student_data, validate_student
from .utils import format_student_info

app = App(token=os.environ["SLACK_BOT_TOKEN"])

@app.message("")
def student_grades(message, say):
    if message["text"].lower().startswith("_student"):
        try:
            user = message["text"].split(" ")[1]
            student_data = get_student_data(user)
            if student_data:
                say("User Information:", thread_ts=message["ts"])
                formatted_info = format_student_info(student_data)
                say(formatted_info, thread_ts=message["ts"])
            else:
                say("Invalid student", thread_ts=message["ts"])
        except IndexError:
            say(
                "Invalid command format. Use '_student <username>'",
                thread_ts=message["ts"],
            )


# TODO: def piscine_data

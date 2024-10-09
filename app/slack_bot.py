import os
from slack_bolt import App
from app.api import get_piscine_data, get_student_data
from app.printer import format_student_info

app = App(token=os.environ["SLACK_BOT_TOKEN"])


@app.message("_student")
def get_student(message, say):
    words = message["text"].lower().split()
    if len(words) != 2:
        say(
            "Invalid command format. Use '_student <username>'",
            thread_ts=message["ts"],
        )
        return
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


@app.message("_piscine")
def get_piscine(message, say, client):
    words = message["text"].lower().split()
    if len(words) != 4:
        say(
            "Invalid command format. Use '_piscine <campus> <year> <month>'",
            thread_ts=message["ts"],
        )
        return
    command, campus, year, month = words  # Extract parameters
    campus_caps = campus.title()
    month_caps = month.title()
    try:
        say(
            "🚀 Getting Data for Piscine {month} {year} in {campus}...".format(
                month=month_caps, year=year, campus=campus_caps
            ), thread_ts=message["ts"]
        )
        say(
            "Plase wait... ⌛".format(
            ), thread_ts=message["ts"]
        )
        # Attempt to get piscine data
        piscine_data = get_piscine_data(campus, year, month)

        if not piscine_data:
            say(
                f"No data found for Piscine at {campus} in {month} {year}",
                thread_ts=message["ts"],
            )
            return
        # List to store all usernames
        all_usernames = []

        for student in piscine_data:
            user = student["login"]
            student_data = get_student_data(user)
            if student_data:
                all_usernames.append(user)

        # After collecting all usernames, display them
        if all_usernames:
            usernames_count = len(all_usernames)
            usernames_text = "\n".join(all_usernames)
            say(
                f"Found {usernames_count} usernames for Piscine at {campus} in {month} {year}:\n{usernames_text}",
                thread_ts=message["ts"],
            )
        else:
            say(
                f"No valid usernames found for Piscine at {campus_caps} in {month_caps} {year}",
                thread_ts=message["ts"],
            )
    except Exception as e:
        say(
            f"An error occurred while processing the command: {str(e)}",
            thread_ts=message["ts"],
        )

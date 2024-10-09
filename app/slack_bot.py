import os
import logging
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
            f"🚀 Getting Data for Piscine {month_caps} {year} in {campus_caps}...",
            thread_ts=message["ts"]
        )
        say(
            "Please wait... ⌛",
            thread_ts=message["ts"]
        )
        # Attempt to get piscine data
        piscine_data = get_piscine_data(campus, year, month)

        if piscine_data is None:
            say(
                f"Failed to retrieve data for Piscine at {campus_caps} in {month_caps} {year}. Check logs for details.",
                thread_ts=message["ts"],
            )
            return
        elif not piscine_data:
            say(
                f"No data found for Piscine at {campus_caps} in {month_caps} {year}",
                thread_ts=message["ts"],
            )
            return

        # List to store all usernames and full names
        all_student_info = []

        for student in piscine_data:
            username = student["login"]
            full_name = f"{student['first_name']} {student['last_name']}"
            all_student_info.append(f"{username}\t{full_name}")

        # After collecting all student info, display them
        if all_student_info:
            student_count = len(all_student_info)
            student_info_text = "\n".join(all_student_info)
            say(
                f"Found {student_count} students for Piscine at {campus_caps} in {month_caps} {year}:\n{student_info_text}",
                thread_ts=message["ts"],
            )
        else:
            say(
                f"No valid student information found for Piscine at {campus_caps} in {month_caps} {year}",
                thread_ts=message["ts"],
            )
    except Exception as e:
        logging.error(f"Error in get_piscine: {str(e)}")
        say(
            f"An error occurred while processing the command. Check logs for details.",
            thread_ts=message["ts"],
        )

import os
import json
import logging
from slack_bolt import App
from app.api import get_piscine_data, get_student_data, get_student_location
from app.printer import format_student_info

app = App(token=os.environ["SLACK_BOT_TOKEN"])

piscine_data = {}


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
    if len(words) < 4 or len(words) > 5:
        say(
            "Invalid command format. Use '_piscine <campus> <year> <month> [project]'",
            thread_ts=message["ts"],
        )
        return

    command, campus, year, month, *project = words  # Extract parameters
    project = project[0] if project else None  # Get project if provided

    campus_caps = campus.title()
    month_caps = month.title()

    try:
        say(
            f"⌛ Getting Data for Piscine *{month_caps} {year}* in *{campus_caps}*{' for project ' + project if project else ''}...",
            thread_ts=message["ts"],
        )
        # Attempt to get piscine data
        piscine_data = get_piscine_data(campus, year, month)

        if piscine_data is None:
            say(
                f"Failed to retrieve data for Piscine at *{campus_caps}* in *{month_caps} {year}*. *Check logs* for details.",
                thread_ts=message["ts"],
            )
            return
        elif not piscine_data:
            say(
                f"No data found for Piscine at *{campus_caps}* in *{month_caps} {year}*",
                thread_ts=message["ts"],
            )
            return

        # List to store all usernames and full names
        all_student_info = []

        for student in piscine_data:
            username = student["login"]
            full_name = f"{student['first_name']} {student['last_name']}"

            # If project is specified, check if the student has completed it
            if project:
                if not any(p["slug"] == project for p in student.get("projects", [])):
                    continue

            all_student_info.append((username, full_name))

        # Sort the list based on usernames
        all_student_info.sort(key=lambda x: x[0].lower())

        # After collecting and sorting all student info, display them
        if all_student_info:
            student_count = len(all_student_info)
            student_info_text = "\n".join(
                [
                    f"*{username}*\t{full_name}"
                    for username, full_name in all_student_info
                ]
            )
            say(
                f"*Piscine {month_caps} {year} in {campus_caps}*{' for project ' + project if project else ''}:\n`{student_count}` students\n\n{student_info_text}",
                thread_ts=message["ts"],
            )
        else:
            say(
                f"No valid student information found for Piscine at *{campus_caps}* in *{month_caps} {year}*{' for project ' + project if project else ''}",
                thread_ts=message["ts"],
            )
    except Exception as e:
        logging.error(f"Error in get_piscine: {str(e)}")
        say(
            f"An error occurred while processing the command. *Check logs* for details.",
            thread_ts=message["ts"],
        )


import json
import logging


@app.message("_locate")
def locate_student(message, say):
    words = message["text"].lower().split()
    if len(words) != 2:
        say(
            "Invalid command format. Use '_locate <student_name>'",
            thread_ts=message["ts"],
        )
        return

    student_name = words[1]

    try:
        location = get_student_location(student_name)

        if location:
            say(
                f"🎒 The student *{student_name}* is located in cluster: 💻 *{location}*",
                thread_ts=message["ts"],
            )
        else:
            say(
                f"No location found for student *{student_name}*",
                thread_ts=message["ts"],
            )
    except Exception as e:
        logging.error(f"Error in locate_student: {str(e)}")
        say(
            f"An error occurred while locating the student. *Check logs* for details.",
            thread_ts=message["ts"],
        )

import os
import logging
from pprint import pprint
from slack_bolt import App
from app.api import get_piscine_data, get_student_data, get_student_location
from app.printer import format_student_info
from warning import warning_status

app = App(token=os.environ["SLACK_BOT_TOKEN"])


@app.message("_piscine")
def get_piscine(message, say, client):
    words = message["text"].lower().split()
    if len(words) < 4 or len(words) > 5:
        say(
            """
            Invalid command format. Use '_piscine <campus> <year> <month> [filter]'
            optional filters : warn, (...)
            """,
            thread_ts=message["ts"],
        )
        return

    command, campus, year, month, *filter = words  # Extract parameters
    filter = filter[0] if filter else None  # Get filter if provided

    campus_caps = campus.title()
    month_caps = month.title()

    try:
        say(
            f"⌛ Getting Data for Piscine *{month_caps} {year}* in *{campus_caps}*{' filtered by ' + filter if filter else ''}...",
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
        all_student_info = []

        # print(f"=> {len(piscine_data)} students found")
        for student in piscine_data:
            username = student["login"]
            full_name = f"{student['first_name']} {student['last_name']}"

            # If filter is specified, check if the student has completed it
            # if filter:
            #     if not any(p["slug"] == filter for p in student.get("projects", [])):
            #         continue

            # Check for warning status
            print(f"=> {warning_status(student)}")
            if len(words) == 5 and words[4] == "warn":
                print(f"=> {warning_status}")
                if warning_status(student) == 1:
                    all_student_info.append((username, full_name))
            else:
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
                f"*Piscine {month_caps} {year} in {campus_caps}*{' for filter ' + filter if filter else ''}:\n`{student_count}` students\n\n{student_info_text}",
                thread_ts=message["ts"],
            )
        else:
            say(
                f"No students found matching the criteria for Piscine {month_caps} {year} in {campus_caps}{' for filter ' + filter if filter else ''}.",
                thread_ts=message["ts"],
            )
    except Exception as e:
        logging.error(f"Error in get_piscine: {str(e)}")
        say(
            f"An error occurred while processing the command. *Check logs* for details.",
            thread_ts=message["ts"],
        )


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

@app.message("_locate")
def locate_student(message, say):
    words = message["text"].lower().split()
    if len(words) < 2 or len(words) > 3:
        say(
            "Invalid command format. Use '_locate <student_name_or_computer_id> [campus]'",
            thread_ts=message["ts"],
        )
        return

    identifier = words[1]
    campus = words[2] if len(words) == 3 else None
    try:
        student_name, location = get_student_location(identifier, campus)
        if identifier.startswith("c") and identifier.find("r") != -1 and identifier.find("s") != -1:
            say(
                f"💻 The computer *{identifier}* is being used by : 🎒 *{student_name}*",
                thread_ts=message["ts"],
            )
        else:
            say(
                f"🎒 The student *{student_name}* is on cluster: 💻 *{location}*",
                thread_ts=message["ts"],
            )
    except Exception as e:
        logging.error(f"Error in locate_student: {str(e)}")
        say(
            f"An error occurred while locating the student or computer. *Check logs* for details.",
            thread_ts=message["ts"],
        )

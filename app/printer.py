from .warning import warning_status

def format_student_info(student_data):
	first_name = student_data["first_name"]
	last_name = student_data["last_name"]
	login = student_data["login"]
	cursus = student_data["cursus_users"][-1]["cursus"]["name"]
	level = student_data["cursus_users"][-1]["level"]
	projects = student_data["projects_users"]
	location = student_data["location"]
	blackhole = student_data["cursus_users"][-1]["blackholed_at"]
	small_image_url = student_data["image"]["versions"]["small"]

	exams = [
		project
		for project in student_data["projects_users"]
		if "Exam" in project["project"]["name"]
	]
	exams_str = "\n".join(
		[
			f">{p['project']['name']}:  `{p['final_mark'] or 'In Progress'}`"
			for p in exams
		]
	)

	only_projects = [
		project
		for project in projects
		if "Exam" not in project["project"]["name"]
	]
	recent_projects = sorted(
		only_projects, key=lambda x: x["marked_at"] or "", reverse=True
	)[:10]
	projects_str = "\n".join(
		[
			f">{p['project']['name']}:  `{p['final_mark'] or 'In Progress'}`"
			for p in recent_projects
		]
	)

	warning = warning_status(student_data)
	match warning:
		case (1):
			warning_msg = "🚨 (_Possibly cheating_)"
		case (2):
			warning_msg = "🦮 (_Needs help_)"
		case _:
			warning_msg = "🟢 (_No flags raised_)"

	return f"""

*User:*     `{login}`
*Name:*    `{first_name} {last_name}`
*Cluster:* `{location}`
*Cursus:*   `{cursus}`
*Level:*     `{level:.2f}`
*Blackhole:* `{blackhole or 'N/A'}`


📂 *Recent Projects :*
{projects_str}


📝 *Exams :* 
{exams_str}

*Warning:* {warning_msg}

*User Photo:* {small_image_url}
"""

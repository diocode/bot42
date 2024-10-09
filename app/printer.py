from .warning import warning_status

def format_student_info(student_data):
	first_name = student_data["first_name"]
	last_name = student_data["last_name"]
	login = student_data["login"]
	cursus = student_data["cursus_users"][-1]["cursus"]["name"]
	level = student_data["cursus_users"][-1]["level"]
	projects = student_data["projects_users"]
	location = student_data["location"]
	small_image_url = student_data["image"]["versions"]["small"]

	progress_data = {}

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

	# Fill progress_data with exam results
	for exam in exams:
		progress_data[exam['project']['name']] = exam.get('final_mark', 'In Progress')

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

	# Fill progress_data with project results
	for project in recent_projects:
		progress_data[project['project']['name']] = project.get('final_mark', 'In Progress')

	return f"""

*User:*     `{login}`
*Name:*    `{first_name} {last_name}`
*Cluster:* `{location}`
*Cursus:*   `{cursus}`
*Level:*     `{level:.2f}`


📂 *Recent Projects :*
{projects_str}


📝 *Exams :* 
{exams_str}

*Warning:* {warning_status(progress_data)}

*User Photo:* {small_image_url}
"""

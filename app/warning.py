from pprint import pprint
from datetime import datetime, timedelta

def get_project_data(student_data):
	projects = student_data["projects_users"]
	progress_data = {}

	exams = [
		project
		for project in student_data["projects_users"]
		if "Exam" in project["project"]["name"]
	]
	# Fill progress_data with exam results
	for exam in exams:
		progress_data[exam['project']['name']] = exam.get('final_mark', 'In Progress')
	
	only_projects = [
		project
		for project in projects
		if "Exam" not in project["project"]["name"]
	]
	# Fill progress_data with project results
	for project in only_projects:
		progress_data[project['project']['name']] = project.get('final_mark', 'In Progress')

	return progress_data

def get_timeline(student_data):
	start_date = datetime.strptime(student_data["cursus_users"][-1]["created_at"], "%Y-%m-%dT%H:%M:%S.%fZ")
	cur_date = datetime.now()

	days_difference = (cur_date - start_date).days
	week = (days_difference // 7) + 1
	if week > 4:
		week = 4
	
	day = cur_date.weekday()
	day_str = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"][day]

	return week, day_str

def	warning_status(student_data):
	projects = student_data["projects_users"]
	week, day = get_timeline(student_data)
	progress_data = get_project_data(student_data)
	student_project_avg = 0
	student_exam_avg = 0
	nbr_projs = 0

	for project_name, score in progress_data.items():
			if project_name.startswith("C Piscine C" or "C Piscine Shell") and isinstance(score, int):
				student_project_avg += score
				nbr_projs += 1

			if "Exam" in project_name:
				if isinstance(score, int):
					student_exam_avg += score

	student_project_avg /= nbr_projs
	
	match week:
		case (1):
			avg_project = "C Piscine C 01"
			exam_avg = 26
			if "Exam C 00" in progress_data:
				student_exam_avg = progress_data["Exam C 00"]
		case (2):
			avg_project = "C Piscine C 03"
			exam_avg = 29
			if "Exam C 01" in progress_data:
				student_exam_avg = progress_data["Exam C 01"]

		case (3):
			avg_project = "C Piscine C 05"
			exam_avg = 30
			if "Exam C 02" in progress_data:
				student_exam_avg = progress_data["Exam C 02"]
		case _:
			avg_project = "C Piscine C 07"
			exam_avg = 34
			if "C Piscine Final Exam" in progress_data:
				student_exam_avg = progress_data["C Piscine Final Exam"]
	
	# Check if the exam's score average is below the week's average and the project's score average is above the week's average or the project's score average is 90
	if exam_avg > student_exam_avg:
		if avg_project in progress_data or student_project_avg >= 90:
			return 1
	return 3

'''
Triggers for cheating:

1. If pisciner's projects delivered are above the week's average
2. If pisciner's project's score average is 90
3. If pisciner's exam's score average is below the week's average 
	and the project's score average is above the week's average

Triggers for helping:

1. If pisciner hasn't delivered Shell00 and C00 in week 2 (tuesday)
2. If pisciner hasn't delivered C01 and C02 in week 3 (tuesday)
3. If pisciner hasn't delivered C03 and C04 in week 4 (tuesday)

'''

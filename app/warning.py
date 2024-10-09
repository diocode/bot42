from pprint import pprint

def	warning_status(progress_data):

	project_lvl = 0
	exam_lvl = 0
	nbr_exams = 0
	for project_name, score in progress_data.items():
		if project_name.startswith("C Piscine C") and isinstance(score, int):
			project_lvl += score

		if "Exam" in project_name:
			nbr_exams += 1
			if isinstance(score, int):
				exam_lvl += score

	#print(f"Projects:{project_lvl} \nExams:{exam_lvl} \nTotal Exams:{nbr_exams}")

	if nbr_exams == 1 and project_lvl > 150 and exam_lvl < 30:
		return "🚩(_possibly cheating_)"

	if nbr_exams == 2 and project_lvl > 300 and exam_lvl < 30:
		return "🚩(_possibly cheating_)"
	
	if nbr_exams == 3 and project_lvl > 400 and exam_lvl < 60:
		return "🚩(_possibly cheating_)"
	
	if nbr_exams == 4 and project_lvl > 400 and exam_lvl < 60:
		return "🚩(_possibly cheating_)"

	return "🏳️ (_not cheating_)"
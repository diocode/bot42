def format_student_info(student_data):
    first_name = student_data["first_name"]
    last_name = student_data["last_name"]
    login = student_data["login"]
    cursus = student_data["cursus_users"][-1]["cursus"]["name"]
    level = student_data["cursus_users"][-1]["level"]
    projects = student_data["projects_users"]
    exams = [
        project
        for project in student_data["projects_users"]
        if "Exam" in project["project"]["name"]
    ]
    exams_str = "\n".join(
        [
            f"- {p['project']['name']}: {p['final_mark'] or 'In Progress'}"
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
            f"- {p['project']['name']}: {p['final_mark'] or 'In Progress'}"
            for p in recent_projects
        ]
    )
    return f"""
🎒 {login}
aka. {first_name} {last_name} 
🚀 Cursus: {cursus}
🎇 Level: {level:.2f}

📟 Recent Projects : 
{projects_str}

📝 Exams : 
{exams_str}
    """

import json


def load_projects():
    with open("data/projects.json", "r", encoding="utf-8") as file:
        return json.load(file)


def recommend_projects(missing_skills):
    projects = load_projects()

    recommendations = []

    for project in projects:
        project_skills = {
            skill.lower() for skill in project["skills"]
        }

        if any(skill.lower() in project_skills for skill in missing_skills):
            recommendations.append(project)

    return recommendations
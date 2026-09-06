import json


def load_skills():
    with open("data/skills.json", "r", encoding="utf-8") as file:
        return json.load(file)


def extract_skills(text):
    skills = load_skills()

    found_skills = []

    text_lower = text.lower()

    for skill in skills:
        if skill.lower() in text_lower:
            found_skills.append(skill)

    return found_skills
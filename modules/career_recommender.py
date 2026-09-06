import json


def load_careers():
    with open("data/careers.json", "r", encoding="utf-8") as file:
        return json.load(file)


def recommend_careers(user_skills):
    careers = load_careers()

    results = []

    user_skills_lower = {skill.lower() for skill in user_skills}

    for career, required_skills in careers.items():
        matched_skills = [
            skill
            for skill in required_skills
            if skill.lower() in user_skills_lower
        ]

        score = (len(matched_skills) / len(required_skills)) * 100

        results.append({
            "career": career,
            "score": round(score, 2),
            "matched_skills": matched_skills,
            "missing_skills": [
                skill
                for skill in required_skills
                if skill.lower() not in user_skills_lower
            ]
        })

    results.sort(key=lambda x: x["score"], reverse=True)

    return results
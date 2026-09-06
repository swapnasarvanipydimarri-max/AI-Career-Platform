def calculate_skill_gap(user_skills, required_skills):
    user_skills_lower = {skill.lower() for skill in user_skills}

    matched_skills = [
        skill for skill in required_skills
        if skill.lower() in user_skills_lower
    ]

    missing_skills = [
        skill for skill in required_skills
        if skill.lower() not in user_skills_lower
    ]

    readiness_score = (
        len(matched_skills) / len(required_skills) * 100
        if required_skills
        else 0
    )

    return {
        "matched_skills": matched_skills,
        "missing_skills": missing_skills,
        "readiness_score": round(readiness_score, 2)
    }
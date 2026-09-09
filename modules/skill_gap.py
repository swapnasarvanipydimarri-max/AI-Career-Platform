def calculate_skill_gap(user_skills, career_skills):
    """
    Compare user skills with the skills required for a career.
    """

    user_skills_lower = {
        skill.strip().lower()
        for skill in user_skills
    }

    career_skills_lower = {
        skill.strip().lower()
        for skill in career_skills
    }

    matched_skills = [
        skill for skill in career_skills
        if skill.strip().lower() in user_skills_lower
    ]

    missing_skills = [
        skill for skill in career_skills
        if skill.strip().lower() not in user_skills_lower
    ]

    total_required = len(career_skills)

    if total_required > 0:
        coverage_percentage = (
            len(matched_skills) / total_required
        ) * 100
    else:
        coverage_percentage = 0

    return {
        "matched_skills": matched_skills,
        "missing_skills": missing_skills,
        "coverage_percentage": round(
            coverage_percentage, 2
        ),
        "total_required_skills": total_required
    }
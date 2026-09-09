def analyze_job_skill_gap(user_skills, required_skills):
    """
    Perform a detailed job-oriented skill gap analysis.
    """

    user_skills_lower = {
        skill.strip().lower()
        for skill in user_skills
    }

    matched_skills = []
    missing_skills = []

    for skill in required_skills:

        skill_clean = skill.strip()

        if skill_clean.lower() in user_skills_lower:

            matched_skills.append(skill_clean)

        else:

            missing_skills.append(skill_clean)

    total_required = len(required_skills)

    if total_required > 0:

        coverage = (
            len(matched_skills)
            / total_required
        ) * 100

    else:

        coverage = 0

    # Assign priority to missing skills.
    priority_skills = []

    for index, skill in enumerate(
        missing_skills
    ):

        if index < 3:

            priority = "High"

        elif index < 6:

            priority = "Medium"

        else:

            priority = "Low"

        priority_skills.append({
            "skill": skill,
            "priority": priority
        })

    return {
        "required_skills": required_skills,
        "matched_skills": matched_skills,
        "missing_skills": missing_skills,
        "coverage_percentage": round(
            coverage,
            2
        ),
        "priority_skills": priority_skills
    }
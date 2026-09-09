def calculate_skill_proficiency(user_skills, resume_text):
    """
    Estimate skill proficiency based on how frequently
    each skill appears in the resume.
    """

    text = resume_text.lower()

    proficiency = []

    for skill in user_skills:

        skill_lower = skill.lower()

        count = text.count(skill_lower)

        if count >= 4:
            level = "Advanced"
            score = 90

        elif count >= 2:
            level = "Intermediate"
            score = 70

        else:
            level = "Beginner"
            score = 40

        proficiency.append({
            "skill": skill,
            "level": level,
            "score": score
        })

    return proficiency
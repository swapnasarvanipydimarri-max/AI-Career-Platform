def generate_career_plan(
    target_career,
    current_skills,
    missing_skills
):
    """
    Generate a personalized 30/60/90-day career plan.
    """

    current_skills = [
        skill.strip()
        for skill in current_skills
        if skill.strip()
    ]

    missing_skills = [
        skill.strip()
        for skill in missing_skills
        if skill.strip()
    ]

    # Select the highest-priority skills first.
    priority_skills = missing_skills[:3]

    if not priority_skills:
        priority_skills = [
            "Advanced Practice",
            "Portfolio Development",
            "Interview Preparation"
        ]

    # --------------------------------------------------
    # FIRST 30 DAYS
    # --------------------------------------------------

    days_30 = [
        f"Learn the fundamentals of {skill}"
        for skill in priority_skills
    ]

    days_30.extend([
        f"Create a weekly learning schedule for {target_career}",
        "Practice the newly learned concepts with small exercises"
    ])

    # --------------------------------------------------
    # DAYS 31-60
    # --------------------------------------------------

    days_60 = [
        f"Build a practical project using {skill}"
        for skill in priority_skills
    ]

    days_60.extend([
        "Upload projects to GitHub",
        "Improve your technical portfolio",
        "Practice explaining your projects clearly"
    ])

    # --------------------------------------------------
    # DAYS 61-90
    # --------------------------------------------------

    days_90 = [
        "Update your resume with newly developed skills",
        "Improve your LinkedIn and professional profile",
        f"Practice technical interviews for {target_career}",
        "Apply for suitable internships and entry-level jobs",
        "Continue improving weak areas identified during preparation"
    ]

    return {
        "target_career": target_career,
        "current_skills": current_skills,
        "missing_skills": missing_skills,
        "days_30": days_30,
        "days_60": days_60,
        "days_90": days_90
    }
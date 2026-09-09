def calculate_career_readiness(
    skill_readiness,
    resume_quality,
    career_match
):
    """
    Calculate an overall career readiness score
    using skill readiness, resume quality, and career match.
    """

    overall_score = (
        (skill_readiness * 0.50)
        + (resume_quality * 0.25)
        + (career_match * 0.25)
    )

    return round(overall_score, 2)
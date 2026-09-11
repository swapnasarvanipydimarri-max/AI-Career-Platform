def calculate_overall_score(readiness_score, job_match_score):
    """
    Calculate an overall career score from readiness
    and job-match scores.
    """
    scores = []

    if readiness_score is not None:
        scores.append(float(readiness_score))

    if job_match_score is not None:
        scores.append(float(job_match_score))

    if not scores:
        return None

    return round(sum(scores) / len(scores), 2)


def get_readiness_label(score):
    """
    Convert a readiness score into a simple category.
    """
    if score is None:
        return "Not Available"

    score = float(score)

    if score >= 80:
        return "Highly Ready"

    if score >= 60:
        return "Moderately Ready"

    if score >= 40:
        return "Needs Improvement"

    return "Needs Significant Improvement"


def get_match_label(score):
    """
    Convert a job-match score into a simple category.
    """
    if score is None:
        return "Not Available"

    score = float(score)

    if score >= 80:
        return "Excellent Match"

    if score >= 60:
        return "Good Match"

    if score >= 40:
        return "Partial Match"

    return "Low Match"


def build_analysis_summary(
    readiness_score=None,
    job_match_score=None,
    recommended_careers=None,
    skill_gaps=None,
):
    """
    Build a clean summary of career-analysis results.
    """
    recommended_careers = recommended_careers or []
    skill_gaps = skill_gaps or []

    overall_score = calculate_overall_score(
        readiness_score,
        job_match_score,
    )

    return {
        "overall_score": overall_score,
        "readiness_score": readiness_score,
        "readiness_label": get_readiness_label(readiness_score),
        "job_match_score": job_match_score,
        "match_label": get_match_label(job_match_score),
        "recommended_careers": recommended_careers,
        "skill_gaps": skill_gaps,
        "skill_gap_count": len(skill_gaps),
    }
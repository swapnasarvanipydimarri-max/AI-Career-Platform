def analyze_resume(resume_text):
    text = resume_text.lower()

    score = 0
    suggestions = []

    # Resume length
    word_count = len(resume_text.split())

    if word_count >= 300:
        score += 25
    else:
        suggestions.append(
            "Add more relevant details to your resume."
        )

    # Education
    if "education" in text:
        score += 15
    else:
        suggestions.append(
            "Add an Education section."
        )

    # Experience
    if "experience" in text:
        score += 20
    else:
        suggestions.append(
            "Add a Work Experience or Internship section."
        )

    # Projects
    if "project" in text:
        score += 20
    else:
        suggestions.append(
            "Add relevant projects to demonstrate your skills."
        )

    # Skills
    if "skill" in text:
        score += 10
    else:
        suggestions.append(
            "Add a dedicated Skills section."
        )

    # Contact information
    if "@" in resume_text:
        score += 10
    else:
        suggestions.append(
            "Add a professional email address."
        )

    return {
        "score": score,
        "word_count": word_count,
        "suggestions": suggestions
    }
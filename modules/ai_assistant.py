def career_assistant(question, career, skills, missing_skills):

    question_lower = question.lower()

    if "skill" in question_lower:
        return (
            f"For {career}, your current skills include "
            f"{', '.join(skills) if skills else 'no detected skills'}. "
            f"Important skills you can work on include "
            f"{', '.join(missing_skills) if missing_skills else 'no major skill gaps'}."
        )

    if "learn" in question_lower or "roadmap" in question_lower:
        return (
            f"Start by learning the most important missing skills: "
            f"{', '.join(missing_skills[:5]) if missing_skills else 'keep improving your existing skills'}."
        )

    if "project" in question_lower:
        return (
            f"For a {career} career, build projects that demonstrate "
            f"your technical skills and solve real-world problems."
        )

    if "interview" in question_lower:
        return (
            f"Prepare for {career} interviews by practicing technical "
            f"questions, explaining your projects, and preparing behavioral answers."
        )

    return (
        f"Based on your profile, {career} appears to be a suitable career direction. "
        "Focus on closing your skill gaps and building practical projects."
    )
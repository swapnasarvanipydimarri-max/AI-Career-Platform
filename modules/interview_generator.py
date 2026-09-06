def generate_interview_questions(career, skills):
    questions = []

    questions.append(
        f"Tell me about yourself and why you want to become a {career}."
    )

    questions.append(
        f"What experience do you have with {skills[0] if skills else 'your technical skills'}?"
    )

    questions.append(
        f"Why are you interested in a career as a {career}?"
    )

    questions.append(
        "Describe a challenging project you worked on and how you solved the problem."
    )

    questions.append(
        "What are your strengths and weaknesses?"
    )

    questions.append(
        "Where do you see yourself professionally in the next five years?"
    )

    return questions
import streamlit as st
from modules.gemini_ai import ask_gemini


def generate_mock_interview(
    target_career,
    current_skills,
    missing_skills
):
    """
    Generate AI-powered mock interview questions.
    """

    prompt = f"""
You are an expert technical interviewer.

Create a mock interview for a student preparing for:

Target Career:
{target_career}

Current Skills:
{", ".join(current_skills) if current_skills else "No skills detected"}

Missing Skills:
{", ".join(missing_skills) if missing_skills else "No major skill gaps"}

Generate exactly 5 interview questions.

Include:
1. Two technical questions
2. One project-based question
3. One problem-solving question
4. One behavioral question

Return only the questions as a numbered list.
"""

    response = ask_gemini(prompt)

    return response


def evaluate_interview_answer(
    target_career,
    question,
    answer
):
    """
    Use Gemini to evaluate an interview answer.
    """

    prompt = f"""
You are an expert interview evaluator.

Evaluate the following answer from a student interviewing
for a {target_career} position.

Interview Question:
{question}

Student Answer:
{answer}

Provide:

1. Score out of 10
2. What was done well
3. What could be improved
4. A better example answer

Keep the feedback practical and easy for a student to understand.
"""

    return ask_gemini(prompt)


def run_mock_interview(
    target_career,
    current_skills,
    missing_skills
):
    """
    Display an interactive AI mock interview.
    """

    st.subheader("🎤 AI Mock Interview")

    st.write(
        f"Practice an interview for the "
        f"**{target_career}** career."
    )

    if st.button(
        "🤖 Generate Mock Interview",
        key="generate_mock_interview"
    ):

        with st.spinner(
            "🤖 Gemini is preparing your interview..."
        ):

            questions = generate_mock_interview(
                target_career,
                current_skills,
                missing_skills
            )

        st.session_state["mock_questions"] = questions

    if "mock_questions" in st.session_state:

        st.success(
            "✅ Mock interview questions generated!"
        )

        st.write(
            st.session_state["mock_questions"]
        )

        st.divider()

        st.subheader(
            "✍️ Practice Your Answer"
        )

        question = st.text_input(
            "Enter the interview question you want to practice:",
            key="mock_question"
        )

        answer = st.text_area(
            "Write your answer:",
            height=180,
            key="mock_answer"
        )

        if st.button(
            "📊 Evaluate My Answer",
            key="evaluate_mock_answer"
        ):

            if question.strip() and answer.strip():

                with st.spinner(
                    "🧠 AI is evaluating your answer..."
                ):

                    feedback = evaluate_interview_answer(
                        target_career,
                        question,
                        answer
                    )

                st.success(
                    "✅ Interview answer evaluated!"
                )

                st.write(
                    feedback
                )

            else:

                st.warning(
                    "Please enter both a question and an answer."
                )
import time

import streamlit as st
from google import genai


def get_gemini_client():
    api_key = st.secrets["GEMINI_API_KEY"]

    return genai.Client(
        api_key=api_key
    )


def ask_gemini(prompt):
    client = get_gemini_client()

    max_retries = 3

    for attempt in range(max_retries):

        try:
            response = client.models.generate_content(
                model="gemini-3.6-flash",
                contents=prompt
            )

            return response.text

        except Exception as e:

            error_message = str(e)

            if "503" in error_message or "UNAVAILABLE" in error_message:

                if attempt < max_retries - 1:
                    wait_time = 2 ** attempt
                    time.sleep(wait_time)
                    continue

                return (
                    "Gemini is temporarily unavailable because the "
                    "model is experiencing high demand. "
                    "Please try again in a few moments."
                )

            raise e


def analyze_resume_with_ai(resume_text):
    prompt = f"""
You are an expert resume reviewer and career coach.

Analyze the following resume:

{resume_text}

Provide:
1. Overall resume feedback
2. Strengths of the resume
3. Areas that need improvement
4. Missing or weak sections
5. Specific suggestions to make the resume more suitable for job applications

Keep the feedback practical, clear, and easy for a student to understand.
"""

    return ask_gemini(prompt)
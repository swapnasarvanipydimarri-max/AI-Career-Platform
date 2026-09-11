import time

import streamlit as st
from google import genai

from modules.rate_limiter import ai_rate_limiter


def get_gemini_client():
    """
    Create the Gemini API client using the configured API key.
    """
    api_key = st.secrets["GEMINI_API_KEY"]

    return genai.Client(
        api_key=api_key
    )


def ask_gemini(prompt):
    """
    Send a request to Gemini with server-side rate limiting
    and retry handling for temporary service errors.
    """

    if not isinstance(prompt, str):
        raise TypeError("Prompt must be a string.")

    if not prompt.strip():
        raise ValueError("Prompt cannot be empty.")

    # Limit the size of AI requests.
    if len(prompt) > 12000:
        raise ValueError(
            "AI request is too large. "
            "Please reduce the amount of text."
        )

    # Use the Streamlit session as the identifier when available.
    # This prevents one user session from making unlimited requests.
    identifier = st.session_state.get(
        "current_user",
        "anonymous",
    )

    if isinstance(identifier, dict):
        identifier = identifier.get(
            "email",
            "anonymous",
        )

    identifier = str(identifier)

    if not ai_rate_limiter.is_allowed(identifier):
        return (
            "Too many AI requests. "
            "Please wait a little before trying again."
        )

    client = get_gemini_client()

    max_retries = 3

    for attempt in range(max_retries):

        try:
            response = client.models.generate_content(
                model="gemini-3.6-flash",
                contents=prompt,
            )

            return response.text

        except Exception as e:

            error_message = str(e)

            if (
                "503" in error_message
                or "UNAVAILABLE" in error_message
            ):

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
    """
    Analyze a resume using Gemini AI.
    """

    if not isinstance(resume_text, str):
        raise TypeError(
            "Resume text must be a string."
        )

    if not resume_text.strip():
        raise ValueError(
            "Resume text cannot be empty."
        )

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
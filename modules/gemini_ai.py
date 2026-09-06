import streamlit as st
from google import genai


def get_gemini_client():
    api_key = st.secrets["GEMINI_API_KEY"]

    return genai.Client(
        api_key=api_key
    )


def ask_gemini(prompt):
    client = get_gemini_client()

    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=prompt
    )

    return response.text

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
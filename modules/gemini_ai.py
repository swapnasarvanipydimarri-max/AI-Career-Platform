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
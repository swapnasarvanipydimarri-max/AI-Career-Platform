from PyPDF2 import PdfReader
import streamlit as st

from modules.rate_limiter import resume_rate_limiter


def extract_text_from_pdf(file):
    """
    Extract text from a PDF resume with server-side
    rate limiting.
    """

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

    if not resume_rate_limiter.is_allowed(identifier):
        raise RuntimeError(
            "Too many resume-processing requests. "
            "Please wait before uploading another resume."
        )

    reader = PdfReader(file)

    text = ""

    for page in reader.pages:
        page_text = page.extract_text()

        if page_text:
            text += page_text + "\n"

    return text
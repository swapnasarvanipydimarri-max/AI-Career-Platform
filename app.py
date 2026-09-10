import streamlit as st
import pandas as pd

from modules.resume_parser import extract_text_from_pdf
from modules.skill_extractor import extract_skills
from modules.career_recommender import recommend_careers
from modules.skill_gap import calculate_skill_gap
from modules.job_skill_gap import analyze_job_skill_gap
from modules.roadmap import generate_roadmap
from modules.career_plan import generate_career_plan
from modules.project_recommender import recommend_projects
from modules.resume_analyzer import analyze_resume
from modules.resume_improver import generate_resume_improvements
from modules.interview_generator import generate_interview_questions
from modules.mock_interview import run_mock_interview
from modules.job_matcher import calculate_job_match
from modules.gemini_ai import ask_gemini, analyze_resume_with_ai
from modules.ml_career_predictor import predict_top_careers
from modules.skill_dashboard import calculate_skill_proficiency
from modules.career_readiness import calculate_career_readiness
from modules.dataset_insights import (
    get_dataset_summary,
    get_career_distribution,
    get_top_skills,
)
from modules.course_recommender import recommend_courses


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="AI Career Intelligence",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# PROFESSIONAL CSS
# ============================================================

st.markdown(
    """
    <style>

    .main {
        background-color: #f8fafc;
    }

    .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
        max-width: 1400px;
    }

    section[data-testid="stSidebar"] {
        background-color: #111827;
        border-right: 1px solid #1f2937;
    }

    section[data-testid="stSidebar"] * {
        color: #f9fafb;
    }

    section[data-testid="stSidebar"] div[role="radiogroup"] {
        gap: 6px;
    }

    section[data-testid="stSidebar"] div[role="radiogroup"] label {
        padding: 10px 12px;
        border-radius: 9px;
    }

    section[data-testid="stSidebar"] div[role="radiogroup"] label:hover {
        background-color: #1f2937;
    }

    h1,
    h2,
    h3 {
        color: #111827;
    }

    div[data-testid="stVerticalBlockBorderWrapper"] {
        border-radius: 16px;
    }

    [data-testid="stFileUploader"] {
        background-color: white;
        border-radius: 14px;
        padding: 10px;
        border: 1px solid #e5e7eb;
    }

    .stButton > button {
        border-radius: 9px;
        font-weight: 600;
        min-height: 42px;
    }

    [data-testid="stMetric"] {
        background-color: white;
        padding: 10px;
        border-radius: 12px;
        border: 1px solid #e5e7eb;
    }

    .footer-text {
        text-align: center;
        color: #64748b;
        font-size: 13px;
        padding: 15px;
    }

    .login-container {
        max-width: 500px;
        margin: 60px auto;
        padding: 35px;
        background-color: white;
        border-radius: 18px;
        border: 1px solid #e5e7eb;
        box-shadow: 0 8px 30px rgba(0, 0, 0, 0.08);
    }

    .login-title {
        text-align: center;
        font-size: 32px;
        font-weight: 700;
        color: #111827;
    }

    .login-subtitle {
        text-align: center;
        color: #64748b;
        margin-bottom: 25px;
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# SESSION STATE
# ============================================================

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if "users" not in st.session_state:
    st.session_state.users = {
        "student@example.com": "student123"
    }

if "current_user" not in st.session_state:
    st.session_state.current_user = None

if "resume_processed" not in st.session_state:
    st.session_state.resume_processed = False

if "mock_questions" not in st.session_state:
    st.session_state.mock_questions = None

if "ai_resume_feedback" not in st.session_state:
    st.session_state.ai_resume_feedback = None

if "resume_improvements" not in st.session_state:
    st.session_state.resume_improvements = None

if "job_match_score" not in st.session_state:
    st.session_state.job_match_score = None

if "career_question_answer" not in st.session_state:
    st.session_state.career_question_answer = None

if "generated_interview_questions" not in st.session_state:
    st.session_state.generated_interview_questions = None


# ============================================================
# LOGIN / SIGN UP PAGE
# ============================================================

if not st.session_state.authenticated:

    st.markdown(
        """
        <div class="login-container">

        <div class="login-title">
            🤖 AI Career Intelligence
        </div>

        <div class="login-subtitle">
            Your personalized AI-powered career companion
        </div>

        </div>
        """,
        unsafe_allow_html=True,
    )

    login_tab, signup_tab = st.tabs(
        ["🔐 Login", "📝 Create Account"]
    )

    # ========================================================
    # LOGIN
    # ========================================================

    with login_tab:

        st.subheader("Welcome Back 👋")

        email = st.text_input(
            "Email",
            placeholder="Enter your email",
            key="login_email",
        )

        password = st.text_input(
            "Password",
            type="password",
            placeholder="Enter your password",
            key="login_password",
        )

        if st.button(
            "🔐 Login",
            use_container_width=True,
            key="login_button",
        ):

            email = email.strip().lower()

            if not email or not password:

                st.warning(
                    "Please enter your email and password."
                )

            elif (
                email in st.session_state.users
                and st.session_state.users[email] == password
            ):

                st.session_state.authenticated = True
                st.session_state.current_user = email

                st.success(
                    "✅ Login successful!"
                )

                st.rerun()

            else:

                st.error(
                    "❌ Invalid email or password."
                )

        st.info(
            "Demo account: student@example.com / student123"
        )

    # ========================================================
    # SIGN UP
    # ========================================================

    with signup_tab:

        st.subheader("Create Your Account 🚀")

        new_email = st.text_input(
            "Email",
            placeholder="Enter your email",
            key="signup_email",
        )

        new_password = st.text_input(
            "Password",
            type="password",
            placeholder="Create a password",
            key="signup_password",
        )

        confirm_password = st.text_input(
            "Confirm Password",
            type="password",
            placeholder="Re-enter your password",
            key="signup_confirm_password",
        )

        if st.button(
            "📝 Create Account",
            use_container_width=True,
            key="signup_button",
        ):

            new_email = new_email.strip().lower()

            if not new_email or not new_password:

                st.warning(
                    "Please fill in all required fields."
                )

            elif "@" not in new_email:

                st.warning(
                    "Please enter a valid email address."
                )

            elif len(new_password) < 6:

                st.warning(
                    "Password must contain at least 6 characters."
                )

            elif new_password != confirm_password:

                st.error(
                    "❌ Passwords do not match."
                )

            elif new_email in st.session_state.users:

                st.error(
                    "❌ An account with this email already exists."
                )

            else:

                st.session_state.users[new_email] = new_password

                st.success(
                    "✅ Account created successfully! "
                    "Please go to the Login tab."
                )

    st.stop()


# ============================================================
# LOGOUT SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown(
        f"""
        <div style="
            background-color:#1f2937;
            padding:12px;
            border-radius:10px;
            margin-bottom:15px;
        ">
            👤 <b>Logged in as</b><br>
            <span style="font-size:12px;">
                {st.session_state.current_user}
            </span>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if st.button(
        "🚪 Logout",
        use_container_width=True,
        key="logout_button",
    ):

        st.session_state.authenticated = False
        st.session_state.current_user = None

        st.rerun()


# ============================================================
# SHARED VARIABLES
# IMPORTANT:
# These are initialized before ANY conditional use.
# ============================================================

uploaded_file = None

resume_text = ""

user_skills = []

career_results = []

resume_analysis = {
    "score": 0,
    "word_count": 0,
    "suggestions": [],
}

top_career = None

required_skills = []

gap = {
    "matched_skills": [],
    "missing_skills": [],
    "coverage_percentage": 0,
    "total_required_skills": 0,
}

overall_readiness = 0


# ============================================================
# SIDEBAR NAVIGATION
# ============================================================

with st.sidebar:

    st.markdown(
        """
        <div style="text-align:center; padding:10px 4px 20px 4px;">
            <div style="font-size:42px;">🤖</div>

            <div style="font-size:24px; font-weight:700;">
                AI Career
            </div>

            <div style="font-size:24px; font-weight:700;">
                Intelligence
            </div>

            <div style="color:#9ca3af; font-size:13px; margin-top:8px;">
                Your personalized career companion
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.divider()

    st.markdown("### 🧭 Navigation")

    page = st.radio(
        "Navigate",
        [
            "🏠 Dashboard",
            "📄 Resume Intelligence",
            "🎯 Career Intelligence",
            "🚀 Career Development",
            "💼 Job Preparation",
            "🤖 AI Assistant",
        ],
        label_visibility="collapsed",
    )


# ============================================================
# MAIN HEADER
# ============================================================

st.title("🤖 AI Career Intelligence")

st.caption(
    "AI-powered resume analysis, career discovery, skill-gap intelligence, "
    "career development, and job preparation."
)


# ============================================================
# WELCOME SECTION
# ============================================================

if page == "🏠 Dashboard" and uploaded_file is None:

    with st.container(border=True):

        st.markdown("### 🤖 AI-POWERED CAREER PLATFORM")

        st.title("Welcome to AI Career Intelligence")

        st.subheader(
            "Turn your resume into your career roadmap."
        )

        st.write(
            "Upload your resume and let AI analyze your skills, "
            "discover suitable careers, identify skill gaps, "
            "recommend learning resources, improve your resume, "
            "and prepare you for real job opportunities."
        )

        st.info(
            "📄 Start by uploading your PDF resume below."
        )


# ============================================================
# RESUME UPLOAD
# ============================================================

st.subheader("📄 Start Your Career Analysis")

uploaded_file = st.file_uploader(
    "Upload your Resume (PDF)",
    type=["pdf"],
    help=(
        "Upload a PDF resume to generate your personalized "
        "career intelligence."
    ),
)


# ============================================================
# PROCESS RESUME
# ============================================================

if uploaded_file is not None:

    try:

        with st.spinner(
            "🔍 Analyzing your resume and building your career profile..."
        ):

            resume_text = extract_text_from_pdf(
                uploaded_file
            )

            user_skills = extract_skills(
                resume_text
            )

            career_results = recommend_careers(
                user_skills
            )

            resume_analysis = analyze_resume(
                resume_text
            )

        st.session_state.resume_processed = True

    except Exception as e:

        st.session_state.resume_processed = False

        st.error(
            f"⚠️ Resume analysis failed: {e}"
        )


# ============================================================
# DETERMINE TOP CAREER
# ============================================================

if career_results:

    top_career = career_results[0]

    required_skills = list(
        dict.fromkeys(
            top_career.get("matched_skills", [])
            + top_career.get("missing_skills", [])
        )
    )

    gap = calculate_skill_gap(
        user_skills,
        required_skills,
    )

    overall_readiness = calculate_career_readiness(
        gap["coverage_percentage"],
        resume_analysis["score"],
        top_career["score"],
    )


# ============================================================
# SIDEBAR PROGRESS
# ============================================================

with st.sidebar:

    st.divider()

    st.markdown("### 📊 Analysis Progress")

    progress_steps = 0

    if uploaded_file is not None:
        progress_steps += 1

    if user_skills:
        progress_steps += 1

    if career_results:
        progress_steps += 1

    if required_skills:
        progress_steps += 1

    if overall_readiness > 0:
        progress_steps += 1

    progress_value = progress_steps / 5

    st.progress(
        min(
            max(progress_value, 0),
            1,
        )
    )

    st.caption(
        f"{int(progress_value * 100)}% • Career intelligence progress"
    )

    st.markdown(
        """
        <div style="
            background-color:#1f2937;
            padding:15px;
            border-radius:12px;
            margin-top:10px;
        ">

        <div style="
            font-size:13px;
            font-weight:700;
            margin-bottom:10px;
        ">
            Career Intelligence Journey
        </div>

        <div style="font-size:12px; margin:7px 0;">
            📄 Resume Analysis
        </div>

        <div style="font-size:12px; margin:7px 0;">
            🧠 Skill Extraction
        </div>

        <div style="font-size:12px; margin:7px 0;">
            🎯 Career Matching
        </div>

        <div style="font-size:12px; margin:7px 0;">
            📊 Skill Gap Intelligence
        </div>

        <div style="font-size:12px; margin:7px 0;">
            🚀 Career Development
        </div>

        <div style="font-size:12px; margin:7px 0;">
            💼 Job Preparation
        </div>

        </div>
        """,
        unsafe_allow_html=True,
    )

    st.divider()

    st.caption(
        "AI Career Platform • Resume • Skills • Careers • Jobs • AI"
    )


# ============================================================
# DASHBOARD — NO RESUME
# ============================================================

if uploaded_file is None and page == "🏠 Dashboard":

    st.subheader("🚀 Your AI Career Journey")

    st.write(
        "Our platform combines resume intelligence, machine learning, "
        "skill-gap analysis, and generative AI to help you understand "
        "where you are and what to do next."
    )

    st.divider()

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        with st.container(border=True):

            st.markdown("### 📄 Resume Intelligence")

            st.write(
                "Analyze resume quality, structure, skills, "
                "and improvement opportunities."
            )

    with col2:

        with st.container(border=True):

            st.markdown("### 🎯 Career Intelligence")

            st.write(
                "Discover careers that match your current "
                "skills and profile."
            )

    with col3:

        with st.container(border=True):

            st.markdown("### 📊 Skill Intelligence")

            st.write(
                "Identify your strengths and the skills "
                "you need to develop."
            )

    with col4:

        with st.container(border=True):

            st.markdown("### 💼 Job Preparation")

            st.write(
                "Match jobs, practice interviews, and "
                "prepare for your target career."
            )

    st.divider()

    # ========================================================
    # DATASET INSIGHTS
    # ========================================================

    st.header("📊 Career Dataset Insights")

    st.caption(
        "Insights from the career profiles dataset used "
        "by the machine-learning prediction system."
    )

    try:

        dataset_summary = get_dataset_summary()

        col1, col2 = st.columns(2)

        with col1:

            st.metric(
                "Career Profiles",
                dataset_summary["total_profiles"],
            )

        with col2:

            st.metric(
                "Dataset Columns",
                dataset_summary["total_columns"],
            )

        st.subheader(
            "💼 Most Common Career Profiles"
        )

        career_distribution = get_career_distribution()

        if not career_distribution.empty:

            st.bar_chart(
                career_distribution
            )

        else:

            st.info(
                "No career distribution data available."
            )

        st.subheader(
            "🧠 Most Common Skills"
        )

        top_skills = get_top_skills()

        if top_skills:

            skills_df = pd.DataFrame(
                top_skills,
                columns=[
                    "Skill",
                    "Profiles",
                ],
            )

            st.bar_chart(
                skills_df.set_index("Skill")
            )

        else:

            st.info(
                "No skill data available."
            )

    except Exception as e:

        st.error(
            f"⚠️ Dataset insights could not be loaded: {e}"
        )


# ============================================================
# DASHBOARD — RESUME UPLOADED
# ============================================================

if uploaded_file is not None and page == "🏠 Dashboard":

    st.success(
        "✅ Your career profile has been generated successfully!"
    )

    with st.container(border=True):

        st.markdown("## 🤖 AI Career Intelligence")

        st.write(
            "Your personalized career profile has been generated "
            "from your resume, skills, career-match analysis, "
            "and readiness indicators."
        )

    st.divider()

    st.subheader("📊 Career Intelligence Overview")

    col1, col2, col3, col4 = st.columns(4)

    career_score = (
        top_career["score"]
        if top_career
        else 0
    )

    with col1:

        st.metric(
            "🎯 Career Readiness",
            f"{overall_readiness}%",
        )

    with col2:

        st.metric(
            "🧠 Skill Coverage",
            f"{gap['coverage_percentage']}%",
        )

    with col3:

        st.metric(
            "📄 Resume Quality",
            f"{resume_analysis['score']}%",
        )

    with col4:

        st.metric(
            "💼 Best Career Match",
            f"{career_score}%",
        )

    st.divider()

    st.subheader("📈 Career Progress Overview")

    col1, col2 = st.columns(2)

    with col1:

        st.write("🎯 **Overall Career Readiness**")

        st.progress(
            min(
                max(
                    overall_readiness / 100,
                    0,
                ),
                1,
            )
        )

        st.caption(
            f"{overall_readiness}% overall readiness"
        )

    with col2:

        st.write("🧠 **Skill Coverage**")

        st.progress(
            min(
                max(
                    gap["coverage_percentage"] / 100,
                    0,
                ),
                1,
            )
        )

        st.caption(
            f"{gap['coverage_percentage']}% of required skills"
        )

    col1, col2 = st.columns(2)

    with col1:

        st.write("📄 **Resume Quality**")

        st.progress(
            min(
                max(
                    resume_analysis["score"] / 100,
                    0,
                ),
                1,
            )
        )

        st.caption(
            f"{resume_analysis['score']}% resume quality"
        )

    with col2:

        if top_career:

            st.write(
                f"🎯 **{top_career['career']} Match**"
            )

            st.progress(
                min(
                    max(
                        top_career["score"] / 100,
                        0,
                    ),
                    1,
                )
            )

            st.caption(
                f"{top_career['score']}% career match"
            )

    st.divider()

    if top_career:

        st.subheader("🏆 Your Best Career Match")

        with st.container(border=True):

            st.markdown(
                f"## 🎯 {top_career['career']}"
            )

            st.write(
                "Based on the skills detected from your resume."
            )

            st.metric(
                "Career Match",
                f"{top_career['score']}%",
            )

        col1, col2 = st.columns(2)

        with col1:

            st.subheader("✅ Why You Match")

            if top_career["matched_skills"]:

                for skill in top_career["matched_skills"]:

                    st.success(
                        f"✓ {skill}"
                    )

            else:

                st.info(
                    "No matching skills detected."
                )

        with col2:

            st.subheader("📚 Skills to Develop")

            if top_career["missing_skills"]:

                for skill in top_career["missing_skills"]:

                    st.warning(
                        f"⚠ {skill}"
                    )

            else:

                st.success(
                    "🎉 No major skill gaps!"
                )

    st.divider()

    st.subheader(
        "🏆 Top Career Recommendations"
    )

    if career_results:

        for index, result in enumerate(
            career_results[:3],
            start=1,
        ):

            with st.container(border=True):

                col1, col2, col3 = st.columns(
                    [1, 5, 2]
                )

                with col1:

                    st.markdown(
                        f"### #{index}"
                    )

                with col2:

                    st.write(
                        f"**{result['career']}**"
                    )

                    st.progress(
                        min(
                            max(
                                result["score"] / 100,
                                0,
                            ),
                            1,
                        )
                    )

                with col3:

                    st.metric(
                        "Match",
                        f"{result['score']}%",
                    )


# ============================================================
# RESUME INTELLIGENCE
# ============================================================

if (
    uploaded_file is not None
    and page == "📄 Resume Intelligence"
):

    st.header("📄 Resume Intelligence")

    st.caption(
        "Analyze the quality, structure, skills, and AI "
        "improvement opportunities in your resume."
    )

    st.subheader("⭐ Resume Quality Analysis")

    col1, col2 = st.columns(2)

    with col1:

        st.metric(
            "Resume Quality Score",
            f"{resume_analysis['score']}/100",
        )

        st.progress(
            min(
                max(
                    resume_analysis["score"] / 100,
                    0,
                ),
                1,
            )
        )

    with col2:

        st.metric(
            "Word Count",
            resume_analysis["word_count"],
        )

    if resume_analysis["suggestions"]:

        st.subheader(
            "💡 Improvement Suggestions"
        )

        for suggestion in resume_analysis["suggestions"]:

            st.write(
                f"🔹 {suggestion}"
            )

    else:

        st.success(
            "🎉 Your resume contains all the basic sections!"
        )

    st.divider()

    st.subheader(
        "🧠 Skills Detected from Resume"
    )

    if user_skills:

        st.write(
            ", ".join(user_skills)
        )

    else:

        st.warning(
            "No matching skills were detected."
        )

    st.divider()

    st.subheader(
        "📊 Skill Proficiency Dashboard"
    )

    st.write(
        "Estimated skill proficiency based on skill mentions "
        "in your resume."
    )

    if user_skills:

        try:

            proficiency_data = calculate_skill_proficiency(
                user_skills,
                resume_text,
            )

            if proficiency_data:

                for item in proficiency_data:

                    col1, col2, col3 = st.columns(
                        [3, 2, 1]
                    )

                    score = min(
                        max(
                            float(item["score"]),
                            0,
                        ),
                        100,
                    )

                    with col1:

                        st.write(
                            f"**{item['skill']}**"
                        )

                        st.progress(
                            score / 100
                        )

                    with col2:

                        if item["level"] == "Advanced":

                            st.success(
                                "🟢 Advanced"
                            )

                        elif item["level"] == "Intermediate":

                            st.warning(
                                "🟡 Intermediate"
                            )

                        else:

                            st.info(
                                "🔵 Beginner"
                            )

                    with col3:

                        st.metric(
                            "Score",
                            f"{score:.0f}%",
                        )

            else:

                st.info(
                    "No proficiency data available."
                )

        except Exception as e:

            st.error(
                f"⚠️ Skill proficiency analysis failed: {e}"
            )

    else:

        st.warning(
            "Skill proficiency requires detected skills."
        )

    st.divider()

    st.subheader("🤖 AI Resume Feedback")

    st.write(
        "Use Gemini to receive personalized feedback "
        "on your resume."
    )

    if st.button(
        "✨ Get AI Resume Feedback",
        key="get_ai_resume_feedback_button",
    ):

        try:

            with st.spinner(
                "🤖 Gemini is reviewing your resume..."
            ):

                st.session_state.ai_resume_feedback = (
                    analyze_resume_with_ai(
                        resume_text
                    )
                )

            st.success(
                "✅ AI resume review completed!"
            )

        except Exception as e:

            st.error(
                f"⚠️ AI resume feedback failed: {e}"
            )

    if st.session_state.ai_resume_feedback:

        with st.container(border=True):

            st.write(
                st.session_state.ai_resume_feedback
            )

    st.divider()

    st.subheader(
        "✨ AI Resume Improvement Generator"
    )

    st.write(
        "Generate ATS-friendly resume improvements based on "
        "your target career and skill gaps."
    )

    improvement_career = (
        career_results[0]["career"]
        if career_results
        else "your target career"
    )

    improvement_missing_skills = (
        career_results[0]["missing_skills"]
        if career_results
        else []
    )

    if st.button(
        "🚀 Generate Resume Improvements",
        key="resume_improvement",
    ):

        try:

            with st.spinner(
                "🤖 Gemini is improving your resume..."
            ):

                st.session_state.resume_improvements = (
                    generate_resume_improvements(
                        resume_text,
                        improvement_career,
                        user_skills,
                        improvement_missing_skills,
                    )
                )

            st.success(
                "✅ Resume improvement analysis completed!"
            )

        except Exception as e:

            st.error(
                f"⚠️ Resume improvement failed: {e}"
            )

    if st.session_state.resume_improvements:

        with st.container(border=True):

            st.write(
                st.session_state.resume_improvements
            )

    st.divider()

    with st.expander(
        "📄 View Extracted Resume Text"
    ):

        st.text_area(
            "Resume Content",
            resume_text,
            height=350,
        )


# ============================================================
# CAREER INTELLIGENCE
# ============================================================

if (
    uploaded_file is not None
    and page == "🎯 Career Intelligence"
):

    st.header("🎯 Career Intelligence")

    st.caption(
        "Understand your career matches, skill gaps, "
        "ML predictions, and readiness."
    )

    st.subheader(
        "🤖 Machine Learning Career Prediction"
    )

    if user_skills:

        try:

            with st.spinner(
                "🧠 Machine Learning model is predicting careers..."
            ):

                top_careers = predict_top_careers(
                    user_skills,
                    top_n=3,
                )

            if top_careers:

                for index, career in enumerate(
                    top_careers,
                    start=1,
                ):

                    confidence = min(
                        max(
                            float(career["confidence"]),
                            0,
                        ),
                        100,
                    )

                    with st.container(border=True):

                        col1, col2, col3 = st.columns(
                            [1, 5, 2]
                        )

                        with col1:

                            st.markdown(
                                f"### #{index}"
                            )

                        with col2:

                            st.write(
                                f"**{career['career']}**"
                            )

                            st.progress(
                                confidence / 100
                            )

                        with col3:

                            st.metric(
                                "Confidence",
                                f"{confidence:.0f}%",
                            )

            else:

                st.info(
                    "No ML career predictions were generated."
                )

        except Exception as e:

            st.error(
                f"⚠️ ML prediction could not be completed: {e}"
            )

    else:

        st.warning(
            "ML prediction requires at least one detected skill."
        )

    st.subheader(
        "🎯 Recommended Careers"
    )

    if career_results:

        for result in career_results[:3]:

            with st.container(border=True):

                st.subheader(
                    result["career"]
                )

                st.write(
                    "Career compatibility based on your "
                    "current skill profile."
                )

                st.progress(
                    min(
                        max(
                            result["score"] / 100,
                            0,
                        ),
                        1,
                    )
                )

                st.metric(
                    "Career Match",
                    f"{result['score']}%",
                )

                if result["matched_skills"]:

                    st.write(
                        "✅ **Matched Skills:** "
                        + ", ".join(
                            result["matched_skills"]
                        )
                    )

                if result["missing_skills"]:

                    st.write(
                        "📚 **Skills to Learn:** "
                        + ", ".join(
                            result["missing_skills"]
                        )
                    )

    else:

        st.warning(
            "No career recommendations were generated."
        )

    if career_results:

        st.subheader(
            "📈 Career Match Overview"
        )

        chart_data = {
            result["career"]: result["score"]
            for result in career_results[:5]
        }

        st.bar_chart(
            chart_data
        )

    st.divider()

    st.header(
        "📊 Skill Gap Intelligence"
    )

    st.write(
        "Identify the skills you already have and the "
        "skills required for your top career."
    )

    st.subheader(
        "📈 Skill Coverage"
    )

    st.progress(
        min(
            max(
                gap["coverage_percentage"] / 100,
                0,
            ),
            1,
        )
    )

    st.write(
        f"**Skill Coverage: {gap['coverage_percentage']}%**"
    )

    col1, col2 = st.columns(2)

    with col1:

        st.subheader(
            "✅ Skills You Have"
        )

        if gap["matched_skills"]:

            for skill in gap["matched_skills"]:

                st.success(
                    skill
                )

        else:

            st.info(
                "No required skills matched yet."
            )

    with col2:

        st.subheader(
            "❌ Skills You Need"
        )

        if gap["missing_skills"]:

            for skill in gap["missing_skills"]:

                st.warning(
                    skill
                )

        else:

            st.success(
                "🎉 You have all required skills!"
            )

    st.divider()

    st.header(
        "💼 Detailed Job Skill-Gap Analysis"
    )

    job_gap = analyze_job_skill_gap(
        user_skills,
        required_skills,
    )

    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric(
            "Required Skills",
            len(job_gap["required_skills"]),
        )

    with col2:

        st.metric(
            "Matching Skills",
            len(job_gap["matched_skills"]),
        )

    with col3:

        st.metric(
            "Missing Skills",
            len(job_gap["missing_skills"]),
        )

    st.write(
        f"**Job Skill Coverage: "
        f"{job_gap['coverage_percentage']}%**"
    )

    st.progress(
        min(
            max(
                job_gap["coverage_percentage"] / 100,
                0,
            ),
            1,
        )
    )

    if job_gap["priority_skills"]:

        st.subheader(
            "🔥 Skill Priority"
        )

        for item in job_gap["priority_skills"]:

            if item["priority"] == "High":

                st.error(
                    f"🔴 {item['skill']} — High Priority"
                )

            elif item["priority"] == "Medium":

                st.warning(
                    f"🟡 {item['skill']} — Medium Priority"
                )

            else:

                st.info(
                    f"🔵 {item['skill']} — Low Priority"
                )

    st.divider()

    st.header(
        "🎯 Overall Career Readiness"
    )

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        st.metric(
            "Overall",
            f"{overall_readiness}%",
        )

    with col2:

        st.metric(
            "Skill Readiness",
            f"{gap['coverage_percentage']}%",
        )

    with col3:

        st.metric(
            "Resume Quality",
            f"{resume_analysis['score']}%",
        )

    with col4:

        st.metric(
            "Career Match",
            (
                f"{top_career['score']}%"
                if top_career
                else "0%"
            ),
        )

    st.progress(
        min(
            max(
                overall_readiness / 100,
                0,
            ),
            1,
        )
    )

    if overall_readiness >= 80:

        st.success(
            "🚀 Excellent career readiness!"
        )

    elif overall_readiness >= 60:

        st.warning(
            "👍 Good career readiness. "
            "Focus on your remaining gaps."
        )

    else:

        st.info(
            "📚 Continue developing your skills and resume."
        )

    st.divider()

    st.header(
        "⚖️ Career Comparison"
    )

    career_names = [
        result["career"]
        for result in career_results
    ]

    if len(career_names) >= 2:

        career1 = st.selectbox(
            "Select First Career",
            career_names,
            key="career1",
        )

        career2 = st.selectbox(
            "Select Second Career",
            career_names,
            index=1,
            key="career2",
        )

        if career1 != career2:

            career1_data = next(
                result
                for result in career_results
                if result["career"] == career1
            )

            career2_data = next(
                result
                for result in career_results
                if result["career"] == career2
            )

            col1, col2 = st.columns(2)

            with col1:

                with st.container(border=True):

                    st.subheader(
                        f"🎯 {career1}"
                    )

                    st.metric(
                        "Career Match",
                        f"{career1_data['score']}%",
                    )

                    st.write(
                        "✅ **Skills You Have**"
                    )

                    st.write(
                        ", ".join(
                            career1_data["matched_skills"]
                        )
                        if career1_data["matched_skills"]
                        else "None"
                    )

                    st.write(
                        "📚 **Skills to Learn**"
                    )

                    st.write(
                        ", ".join(
                            career1_data["missing_skills"]
                        )
                        if career1_data["missing_skills"]
                        else "None"
                    )

            with col2:

                with st.container(border=True):

                    st.subheader(
                        f"🚀 {career2}"
                    )

                    st.metric(
                        "Career Match",
                        f"{career2_data['score']}%",
                    )

                    st.write(
                        "✅ **Skills You Have**"
                    )

                    st.write(
                        ", ".join(
                            career2_data["matched_skills"]
                        )
                        if career2_data["matched_skills"]
                        else "None"
                    )

                    st.write(
                        "📚 **Skills to Learn**"
                    )

                    st.write(
                        ", ".join(
                            career2_data["missing_skills"]
                        )
                        if career2_data["missing_skills"]
                        else "None"
                    )

        else:

            st.warning(
                "Please select two different careers."
            )

    else:

        st.info(
            "At least two career recommendations "
            "are required for comparison."
        )


# ============================================================
# CAREER DEVELOPMENT
# ============================================================

if (
    uploaded_file is not None
    and page == "🚀 Career Development"
):

    st.header(
        "🚀 Career Development"
    )

    st.caption(
        "Build the skills, projects, and experience "
        "needed for your target career."
    )

    if top_career:

        st.subheader(
            "🗺️ Personalized Learning Roadmap"
        )

        try:

            roadmap = generate_roadmap(
                gap["missing_skills"]
            )

            if roadmap:

                for item in roadmap:

                    with st.container(border=True):

                        st.subheader(
                            f"Step {item['step']}: {item['skill']}"
                        )

                        st.write(
                            item["recommendation"]
                        )

                        st.link_button(
                            f"📚 Learn {item['skill']}",
                            item["resource"],
                        )

            else:

                st.success(
                    "🎉 No additional roadmap steps are required!"
                )

        except Exception as e:

            st.error(
                f"⚠️ Roadmap generation failed: {e}"
            )

        st.header(
            "📚 Smart Course & Resource Recommendations"
        )

        try:

            course_recommendations = recommend_courses(
                gap["missing_skills"]
            )

            if course_recommendations:

                for course in course_recommendations:

                    with st.container(border=True):

                        col1, col2 = st.columns(
                            [3, 1]
                        )

                        with col1:

                            st.subheader(
                                f"🧠 {course['skill']}"
                            )

                            st.write(
                                f"**Course:** "
                                f"{course['course']}"
                            )

                            st.write(
                                f"**Platform:** "
                                f"{course['platform']}"
                            )

                        with col2:

                            st.link_button(
                                "📚 Open Resource",
                                course["resource"],
                            )

            else:

                st.success(
                    "🎉 No course recommendations are needed."
                )

        except Exception as e:

            st.error(
                f"⚠️ Course recommendations failed: {e}"
            )

        st.header(
            "🗓️ Personalized 30 / 60 / 90-Day Career Plan"
        )

        try:

            career_plan = generate_career_plan(
                top_career["career"],
                user_skills,
                gap["missing_skills"],
            )

            col1, col2, col3 = st.columns(3)

            with col1:

                with st.container(border=True):

                    st.markdown(
                        "### 📅 First 30 Days"
                    )

                    for action in career_plan["days_30"]:

                        st.write(
                            f"🔹 {action}"
                        )

            with col2:

                with st.container(border=True):

                    st.markdown(
                        "### 📅 Days 31–60"
                    )

                    for action in career_plan["days_60"]:

                        st.write(
                            f"🔹 {action}"
                        )

            with col3:

                with st.container(border=True):

                    st.markdown(
                        "### 📅 Days 61–90"
                    )

                    for action in career_plan["days_90"]:

                        st.write(
                            f"🔹 {action}"
                        )

        except Exception as e:

            st.error(
                f"⚠️ Career plan generation failed: {e}"
            )

        st.divider()

        st.header(
            "💡 Recommended Projects"
        )

        try:

            projects = recommend_projects(
                gap["missing_skills"]
            )

            if projects:

                for project in projects[:3]:

                    with st.container(border=True):

                        st.subheader(
                            project["title"]
                        )

                        st.write(
                            project["description"]
                        )

                        st.write(
                            "🛠️ **Skills:** "
                            + ", ".join(
                                project["skills"]
                            )
                        )

            else:

                st.info(
                    "No project recommendations found."
                )

        except Exception as e:

            st.error(
                f"⚠️ Project recommendations failed: {e}"
            )

    else:

        st.warning(
            "A career recommendation is required "
            "to generate your development plan."
        )


# ============================================================
# JOB PREPARATION
# ============================================================

if (
    uploaded_file is not None
    and page == "💼 Job Preparation"
):

    st.header(
        "💼 Job Preparation"
    )

    st.caption(
        "Test your resume against jobs and practice "
        "interviews with AI."
    )

    if top_career:

        st.subheader(
            "🔍 Job Description Matcher"
        )

        job_description = st.text_area(
            "Paste a Job Description",
            height=250,
            placeholder="Paste the job description here...",
            key="job_description",
        )

        if st.button(
            "🔍 Analyze Job Match",
            key="analyze_job_match",
        ):

            if job_description.strip():

                try:

                    with st.spinner(
                        "🔎 Comparing your resume with the job..."
                    ):

                        match_score = calculate_job_match(
                            resume_text,
                            job_description,
                        )

                    st.session_state.job_match_score = min(
                        max(
                            float(match_score),
                            0,
                        ),
                        100,
                    )

                except Exception as e:

                    st.error(
                        f"⚠️ Job matching failed: {e}"
                    )

            else:

                st.warning(
                    "Please paste a job description first."
                )

        if st.session_state.job_match_score is not None:

            match_score = st.session_state.job_match_score

            st.subheader(
                "📊 Job Match Score"
            )

            st.metric(
                "Resume ↔ Job Match",
                f"{match_score:.0f}%",
            )

            st.progress(
                match_score / 100
            )

            if match_score >= 75:

                st.success(
                    "🎉 Excellent match! "
                    "Your resume aligns well with this job."
                )

            elif match_score >= 50:

                st.warning(
                    "👍 Good match, but there are some areas "
                    "you could improve."
                )

            else:

                st.error(
                    "⚠️ Low match. Consider developing "
                    "more relevant skills."
                )

        st.divider()

        st.header(
            "🎤 AI Interview Question Generator"
        )

        if st.button(
            "🎤 Generate Interview Questions",
            key="generate_interview_questions",
        ):

            try:

                with st.spinner(
                    "🤖 Generating interview questions..."
                ):

                    interview_questions = (
                        generate_interview_questions(
                            top_career["career"],
                            user_skills,
                        )
                    )

                st.session_state.generated_interview_questions = (
                    interview_questions
                )

            except Exception as e:

                st.error(
                    f"⚠️ Interview questions could not be generated: {e}"
                )

        if st.session_state.generated_interview_questions:

            st.write(
                f"Practice these questions for a "
                f"**{top_career['career']}** interview:"
            )

            for index, question in enumerate(
                st.session_state.generated_interview_questions,
                start=1,
            ):

                st.write(
                    f"**{index}. {question}**"
                )

        st.divider()

        run_mock_interview(
            top_career["career"],
            user_skills,
            gap["missing_skills"],
        )

    else:

        st.warning(
            "Please upload a resume with detectable "
            "career-related skills first."
        )


# ============================================================
# AI ASSISTANT
# ============================================================

if (
    uploaded_file is not None
    and page == "🤖 AI Assistant"
):

    st.header(
        "🤖 AI Career Assistant"
    )

    st.caption(
        "Ask Gemini for personalized career guidance "
        "based on your resume analysis."
    )

    if top_career:

        with st.container(border=True):

            st.subheader(
                "💬 Your AI Career Mentor"
            )

            st.write(
                "Ask questions about skills, careers, "
                "learning paths, interviews, resumes, "
                "or job preparation."
            )

        question = st.text_input(
            "Ask a career question",
            placeholder=(
                "Example: What skills should I learn next?"
            ),
            key="career_question",
        )

        if st.button(
            "💬 Ask AI Career Assistant",
            key="ask_career_assistant",
        ):

            if question.strip():

                prompt = f"""
You are an expert AI Career Assistant helping a student
plan their career.

Target Career:
{top_career["career"]}

Current Skills:
{", ".join(user_skills) if user_skills else "No skills detected"}

Missing Skills:
{", ".join(gap["missing_skills"]) if gap["missing_skills"] else "No major skill gaps"}

Overall Career Readiness:
{overall_readiness}%

User Question:
{question}

Give a clear, practical, and personalized answer.

Rules:
- Focus on the user's target career.
- Consider their current and missing skills.
- Consider their overall career readiness score.
- Recommend specific actions when appropriate.
- Keep the answer easy for a student to understand.
- Do not invent information about the user's background.
"""

                try:

                    with st.spinner(
                        "🤖 AI Career Assistant is thinking..."
                    ):

                        st.session_state.career_question_answer = (
                            ask_gemini(
                                prompt
                            )
                        )

                    st.success(
                        "✅ AI response generated!"
                    )

                except Exception as e:

                    st.error(
                        f"⚠️ AI Assistant failed: {e}"
                    )

            else:

                st.warning(
                    "Please enter a question first."
                )

        if st.session_state.career_question_answer:

            with st.container(border=True):

                st.write(
                    st.session_state.career_question_answer
                )

    else:

        st.warning(
            "Please upload a resume with detectable "
            "career information first."
        )


# ============================================================
# NO RESUME MESSAGE FOR OTHER PAGES
# ============================================================

if (
    uploaded_file is None
    and page != "🏠 Dashboard"
):

    st.warning(
        "📄 Please upload your resume above "
        "to access this section."
    )


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.markdown(
    """
    <div class="footer-text">
        🤖 <b>AI Career Intelligence Platform</b>
        <br>
        Resume Intelligence • ML Career Prediction •
        Skill Gap Intelligence • Career Development •
        Job Preparation • AI Guidance
    </div>
    """,
    unsafe_allow_html=True,
)


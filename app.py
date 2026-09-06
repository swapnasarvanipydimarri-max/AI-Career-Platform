import streamlit as st

from modules.resume_parser import extract_text_from_pdf
from modules.skill_extractor import extract_skills
from modules.career_recommender import recommend_careers
from modules.skill_gap import calculate_skill_gap
from modules.roadmap import generate_roadmap
from modules.project_recommender import recommend_projects
from modules.resume_analyzer import analyze_resume
from modules.interview_generator import generate_interview_questions
from modules.job_matcher import calculate_job_match
from modules.ai_assistant import career_assistant


# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="AI Career Platform",
    page_icon="🎯",
    layout="wide"
)


# --------------------------------------------------
# HEADER
# --------------------------------------------------

st.title("🎯 AI Career & Skill Gap Intelligence System")

st.caption(
    "AI-powered resume analysis, career recommendations, "
    "skill-gap intelligence, and career planning."
)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.info("📄 Resume Analysis")

with col2:
    st.info("🎯 Career Matching")

with col3:
    st.info("📊 Skill Gap Analysis")

with col4:
    st.info("🗺️ Learning Roadmap")

st.write(
    "Upload your resume to discover your skills, "
    "career matches, skill gaps, learning roadmap, "
    "and recommended projects."
)

st.divider()


# --------------------------------------------------
# RESUME UPLOAD
# --------------------------------------------------

uploaded_file = st.file_uploader(
    "📄 Upload your Resume (PDF)",
    type=["pdf"]
)


# --------------------------------------------------
# RESUME ANALYSIS
# --------------------------------------------------

if uploaded_file is not None:

    with st.spinner("🔍 Analyzing your resume..."):

        resume_text = extract_text_from_pdf(uploaded_file)

        user_skills = extract_skills(resume_text)

        career_results = recommend_careers(user_skills)

    st.success("✅ Resume analyzed successfully!")

    resume_analysis = analyze_resume(resume_text)

    # --------------------------------------------------
    # RESUME QUALITY
    # --------------------------------------------------

    st.header("⭐ Resume Quality Analysis")

    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            "Resume Quality Score",
            f"{resume_analysis['score']}/100"
        )

    with col2:
        st.metric(
            "Word Count",
            resume_analysis["word_count"]
        )

    if resume_analysis["suggestions"]:

        st.subheader("💡 Improvement Suggestions")

        for suggestion in resume_analysis["suggestions"]:
            st.write(f"🔹 {suggestion}")

    else:

        st.success(
            "🎉 Your resume contains all the basic sections!"
        )

    st.divider()

    # --------------------------------------------------
    # RESUME PREVIEW
    # --------------------------------------------------

    with st.expander("📄 View Extracted Resume Text"):

        st.text_area(
            "Resume Content",
            resume_text,
            height=300
        )

    # --------------------------------------------------
    # SKILLS
    # --------------------------------------------------

    st.header("🧠 Your Skills")

    if user_skills:

        st.write(", ".join(user_skills))

    else:

        st.warning(
            "No matching skills were detected."
        )

    st.divider()

    # --------------------------------------------------
    # CAREER RECOMMENDATIONS
    # --------------------------------------------------

    st.header("🎯 Recommended Careers")

    for result in career_results[:3]:

        st.subheader(result["career"])

        col1, col2 = st.columns([3, 1])

        with col1:

            st.progress(
                int(result["score"])
            )

        with col2:

            st.metric(
                "Match",
                f"{result['score']}%"
            )

        if result["matched_skills"]:

            st.write(
                "✅ Matched Skills: "
                + ", ".join(
                    result["matched_skills"]
                )
            )

        else:

            st.write(
                "❌ No matching skills found."
            )

        if result["missing_skills"]:

            st.write(
                "📚 Skills to Learn: "
                + ", ".join(
                    result["missing_skills"]
                )
            )

        st.divider()

    # --------------------------------------------------
    # CAREER ANALYSIS
    # --------------------------------------------------

    if career_results:

        top_career = career_results[0]

        # --------------------------------------------------
        # CAREER MATCH CHART
        # --------------------------------------------------

        st.subheader(
            "📈 Career Match Overview"
        )

        chart_data = {
            result["career"]: result["score"]
            for result in career_results[:5]
        }

        st.bar_chart(chart_data)

        # --------------------------------------------------
        # SKILL GAP ANALYSIS
        # --------------------------------------------------

        st.header("📊 Skill Gap Analysis")

        required_skills = (
            top_career["matched_skills"]
            + top_career["missing_skills"]
        )

        gap = calculate_skill_gap(
            user_skills,
            required_skills
        )

        # --------------------------------------------------
        # SKILL GAP METRICS
        # --------------------------------------------------

        col1, col2, col3 = st.columns(3)

        with col1:

            st.metric(
                "Career Readiness",
                f"{gap['readiness_score']}%"
            )

        with col2:

            st.metric(
                "Skills You Have",
                len(gap["matched_skills"])
            )

        with col3:

            st.metric(
                "Skills to Learn",
                len(gap["missing_skills"])
            )

        # --------------------------------------------------
        # MISSING SKILLS
        # --------------------------------------------------

        st.subheader(
            f"🚀 Skills Needed for {top_career['career']}"
        )

        if gap["missing_skills"]:

            for skill in gap["missing_skills"]:

                st.write(
                    f"🔹 {skill}"
                )

        else:

            st.success(
                "🎉 You already have all required skills!"
            )

        st.divider()

        # --------------------------------------------------
        # LEARNING ROADMAP
        # --------------------------------------------------

        st.header(
            "🗺️ Personalized Learning Roadmap"
        )

        roadmap = generate_roadmap(
            gap["missing_skills"]
        )

        for item in roadmap:

            st.write(
                f"**Step {item['step']}: "
                f"{item['skill']}**"
            )

            st.caption(
                item["recommendation"]
            )

            st.link_button(
                f"📚 Learn {item['skill']}",
                item["resource"]
            )

        st.divider()

        # --------------------------------------------------
        # PROJECT RECOMMENDATIONS
        # --------------------------------------------------

        st.header(
            "💡 Recommended Projects"
        )

        projects = recommend_projects(
            gap["missing_skills"]
        )

        if projects:

            for project in projects[:3]:

                st.subheader(
                    project["title"]
                )

                st.write(
                    project["description"]
                )

                st.write(
                    "🛠️ Skills: "
                    + ", ".join(
                        project["skills"]
                    )
                )

        else:

            st.info(
                "No project recommendations found."
            )

        st.divider()

        # --------------------------------------------------
        # CAREER COMPARISON
        # --------------------------------------------------

        st.header("⚖️ Career Comparison")

        career_names = [
            result["career"]
            for result in career_results
        ]

        if len(career_names) >= 2:

            career1 = st.selectbox(
                "Select First Career",
                career_names,
                key="career1"
            )

            career2 = st.selectbox(
                "Select Second Career",
                career_names,
                index=1,
                key="career2"
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

                    st.subheader(
                        f"🎯 {career1}"
                    )

                    st.metric(
                        "Career Match",
                        f"{career1_data['score']}%"
                    )

                    st.write(
                        "✅ Skills You Have"
                    )

                    st.write(
                        ", ".join(
                            career1_data["matched_skills"]
                        )
                        if career1_data["matched_skills"]
                        else "None"
                    )

                    st.write(
                        "📚 Skills to Learn"
                    )

                    st.write(
                        ", ".join(
                            career1_data["missing_skills"]
                        )
                        if career1_data["missing_skills"]
                        else "None"
                    )

                with col2:

                    st.subheader(
                        f"🚀 {career2}"
                    )

                    st.metric(
                        "Career Match",
                        f"{career2_data['score']}%"
                    )

                    st.write(
                        "✅ Skills You Have"
                    )

                    st.write(
                        ", ".join(
                            career2_data["matched_skills"]
                        )
                        if career2_data["matched_skills"]
                        else "None"
                    )

                    st.write(
                        "📚 Skills to Learn"
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

        st.divider()

        # --------------------------------------------------
        # INTERVIEW QUESTION GENERATOR
        # --------------------------------------------------

        st.header(
            "🎤 AI Interview Question Generator"
        )

        interview_questions = generate_interview_questions(
            top_career["career"],
            user_skills
        )

        st.write(
            f"Practice these questions for a "
            f"**{top_career['career']}** interview:"
        )

        for index, question in enumerate(
            interview_questions,
            start=1
        ):

            st.write(
                f"**{index}. {question}**"
            )

        st.divider()

        # --------------------------------------------------
        # JOB DESCRIPTION MATCHER
        # --------------------------------------------------

        st.header(
            "💼 Job Description Matcher"
        )

        job_description = st.text_area(
            "Paste a Job Description",
            height=250,
            placeholder="Paste the job description here..."
        )

        if st.button("🔍 Analyze Job Match"):

            if job_description.strip():

                match_score = calculate_job_match(
                    resume_text,
                    job_description
                )

                st.subheader(
                    "📊 Job Match Score"
                )

                st.metric(
                    "Resume ↔ Job Match",
                    f"{match_score}%"
                )

                if match_score >= 75:

                    st.success(
                        "🎉 Excellent match! "
                        "Your resume aligns well with this job."
                    )

                elif match_score >= 50:

                    st.warning(
                        "👍 Good match, but there are "
                        "some areas you could improve."
                    )

                else:

                    st.error(
                        "⚠️ Low match. Consider developing "
                        "more relevant skills."
                    )

            else:

                st.warning(
                    "Please paste a job description first."
                )

        st.divider()

        # --------------------------------------------------
        # AI CAREER ASSISTANT
        # --------------------------------------------------

        st.header(
            "🤖 AI Career Assistant"
        )

        question = st.text_input(
            "Ask a career question",
            placeholder="Example: What skills should I learn?"
        )

        if st.button("💬 Ask Assistant"):

            if question.strip():

                answer = career_assistant(
                    question,
                    top_career["career"],
                    user_skills,
                    gap["missing_skills"]
                )

                st.info(answer)

            else:

                st.warning(
                    "Please enter a question first."
                )
from modules.gemini_ai import ask_gemini


def generate_resume_improvements(
    resume_text,
    target_career,
    current_skills,
    missing_skills
):
    """
    Generate AI-powered resume improvement suggestions.
    """

    prompt = f"""
You are an expert resume writer and ATS optimization specialist.

Analyze the following student's resume and suggest specific improvements.

Target Career:
{target_career}

Current Skills:
{", ".join(current_skills) if current_skills else "No skills detected"}

Missing Skills:
{", ".join(missing_skills) if missing_skills else "No major skill gaps"}

Resume:
{resume_text}

Provide the following:

1. Improved Professional Summary
Write a concise, ATS-friendly professional summary suitable
for the target career.

2. Improved Resume Bullet Points
Identify weak or generic resume statements and provide
stronger versions using action verbs and measurable impact
where possible.

3. Skills Section Improvement
Suggest how the student's skills section should be organized.

4. Missing Resume Sections
Identify important sections that appear to be missing.

5. ATS Optimization
Give practical suggestions to improve keyword usage,
formatting, and readability for applicant tracking systems.

6. Overall Resume Improvement Plan
Give 5 specific actions the student should take.

Important rules:
- Do not invent jobs, degrees, certifications, projects, or achievements.
- Do not create fake numbers or statistics.
- Use only information supported by the resume.
- Clearly indicate where the student should add their own
  real information.
- Keep the recommendations practical and student-friendly.
"""

    return ask_gemini(prompt)
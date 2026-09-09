# 🤖 AI Career Intelligence Platform

An AI-powered career guidance platform that analyzes a student's resume, identifies skills, recommends suitable career paths, detects skill gaps, generates personalized learning plans, and provides AI-powered job and interview preparation.

---

## 📌 Project Overview

The **AI Career Intelligence Platform** is a minor project designed to help students and job seekers understand their career readiness and make better career decisions.

The system combines:

- Resume analysis
- Skill extraction
- Career recommendation
- Machine learning career prediction
- Skill-gap analysis
- Career readiness scoring
- Personalized learning roadmaps
- Course recommendations
- Project recommendations
- Job description matching
- AI resume feedback
- AI resume improvement
- AI mock interviews
- AI career assistance

The platform converts a user's resume into a personalized **career intelligence profile**.

---

## 🎯 Objectives

The main objectives of this project are:

1. Analyze resumes automatically.
2. Extract technical and professional skills.
3. Recommend suitable career paths.
4. Predict potential careers using machine learning.
5. Identify missing skills for target careers.
6. Calculate overall career readiness.
7. Generate personalized career development plans.
8. Recommend learning resources and projects.
9. Compare resumes with job descriptions.
10. Provide AI-powered resume improvement suggestions.
11. Generate and evaluate interview questions and answers.
12. Provide personalized career guidance using Gemini AI.

---

## ✨ Key Features

### 📄 1. Resume Intelligence

Users can upload their resume in PDF format.

The system:

- Extracts resume text
- Counts resume words
- Checks important resume sections
- Calculates a resume quality score
- Detects skills
- Provides improvement suggestions

---

### 🧠 2. Skill Extraction

The platform automatically identifies relevant skills from the uploaded resume.

Example skills:

- Python
- SQL
- Machine Learning
- Data Analysis
- Pandas
- NumPy
- Git
- GitHub
- Java
- JavaScript
- React
- AWS
- Docker

---

### 🎯 3. Career Recommendations

The system analyzes the user's detected skills and recommends suitable careers.

The platform provides:

- Career match percentage
- Matching skills
- Missing skills
- Top career recommendations

---

### 🤖 4. Machine Learning Career Prediction

A machine learning model predicts suitable career paths using the career profile dataset.

The system provides the:

- Top career prediction
- Second-best career prediction
- Third-best career prediction
- Prediction confidence

---

### 📊 5. Skill Gap Intelligence

The system compares:

**User Skills vs Required Career Skills**

It identifies:

- Skills already available
- Missing skills
- Skill coverage percentage
- Required skills

This helps users understand what they need to learn for their target career.

---

### 💼 6. Detailed Job Skill-Gap Analysis

The platform performs job-oriented skill-gap analysis.

Missing skills are categorized into:

- 🔴 High Priority
- 🟡 Medium Priority
- 🔵 Low Priority

This helps users decide which skills should be learned first.

---

### 📈 7. Skill Proficiency Dashboard

The platform estimates skill proficiency based on skill mentions in the resume.

Skills are categorized as:

- Beginner
- Intermediate
- Advanced

Each skill receives a proficiency score.

---

### 🚀 8. Career Readiness Score

The platform calculates an overall career readiness score using:

- Skill readiness
- Resume quality
- Career match

The score provides a quick overview of how prepared the user is for their target career.

---

### 🗺️ 9. Personalized Learning Roadmap

The system creates a learning roadmap based on missing skills.

It provides recommended learning steps and resources for developing the required skills.

---

### 📚 10. Smart Course Recommendations

The platform recommends learning resources for missing skills.

Resources can include:

- freeCodeCamp
- W3Schools
- Google Machine Learning resources
- Pandas documentation
- NumPy tutorials
- Git documentation
- GitHub Skills
- Docker documentation
- AWS resources
- MDN
- Khan Academy

---

### 🗓️ 11. 30/60/90-Day Career Plan

The system generates a personalized career development plan.

#### First 30 Days

Focus on:

- Learning fundamentals
- Creating a learning schedule
- Practicing concepts

#### Days 31–60

Focus on:

- Building projects
- Uploading projects to GitHub
- Improving portfolio
- Practicing project explanations

#### Days 61–90

Focus on:

- Updating resume
- Improving professional profiles
- Interview preparation
- Applying for internships and entry-level jobs

---

### 💡 12. Project Recommendations

The platform recommends projects based on missing skills.

Projects help users:

- Practice technical skills
- Build portfolios
- Demonstrate practical knowledge
- Strengthen resumes

---

### 🔍 13. Job Description Matcher

Users can paste a job description into the platform.

The system compares:

**Resume ↔ Job Description**

and generates a job match score.

This helps users understand how well their resume matches a specific job opportunity.

---

### ✨ 14. AI Resume Feedback

Gemini AI analyzes the uploaded resume and provides:

- Overall feedback
- Resume strengths
- Improvement areas
- Missing or weak sections
- Practical suggestions

---

### 📝 15. AI Resume Improvement Generator

The platform can generate personalized resume improvement suggestions.

It provides:

- Improved professional summary
- Improved resume bullet points
- Skills section recommendations
- Missing resume sections
- ATS optimization suggestions
- Overall resume improvement plan

The system is instructed not to invent qualifications, achievements, jobs, or statistics.

---

### 🎤 16. AI Interview Question Generator

The platform generates interview questions based on the user's target career and skills.

Questions can cover:

- Technical knowledge
- Projects
- Problem solving
- Behavioral questions

---

### 🎤 17. AI Mock Interview

Users can practice interview questions generated by Gemini AI.

The platform can also evaluate a user's answer and provide:

- Score out of 10
- Strengths
- Areas for improvement
- Example of a stronger answer

---

### 🤖 18. AI Career Assistant

The AI Career Assistant acts as a personalized career mentor.

Users can ask questions about:

- Career choices
- Skills
- Learning paths
- Resume improvement
- Interviews
- Job preparation
- Career development

The assistant considers the user's:

- Current skills
- Missing skills
- Target career
- Career readiness

---

### 📊 19. Career Dataset Insights

The platform provides insights from the career profile dataset.

It displays:

- Number of career profiles
- Number of dataset columns
- Most common career profiles
- Most common skills

---

## 🏗️ System Architecture

```text
                    ┌──────────────────────┐
                    │      User            │
                    │   Uploads Resume     │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │   Resume Parser      │
                    │      PDF → Text      │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │   Skill Extractor    │
                    └──────────┬───────────┘
                               │
                ┌──────────────┼──────────────┐
                ▼              ▼              ▼
       ┌──────────────┐ ┌──────────────┐ ┌──────────────┐
       │   Career     │ │   Skill Gap  │ │     ML       │
       │ Recommender  │ │   Analysis   │ │ Prediction   │
       └──────┬───────┘ └──────┬───────┘ └──────┬───────┘
              │                │                │
              └────────────────┼────────────────┘
                               ▼
                    ┌──────────────────────┐
                    │ Career Readiness     │
                    │      Score           │
                    └──────────┬───────────┘
                               │
          ┌────────────────────┼─────────────────────┐
          ▼                    ▼                     ▼
 ┌─────────────────┐  ┌──────────────────┐  ┌─────────────────┐
 │ Learning        │  │ Job Preparation  │  │ Gemini AI       │
 │ Roadmap         │  │ & Interviews     │  │ Assistant       │
 └─────────────────┘  └──────────────────┘  └─────────────────┘

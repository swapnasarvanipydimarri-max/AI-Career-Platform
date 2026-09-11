from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class UserProfile:
    """
    Represents a user's career profile.
    """

    email: str
    name: str = ""
    resume_text: str = ""
    skills: List[str] = field(default_factory=list)
    career_interests: List[str] = field(default_factory=list)
    education: str = ""
    experience_years: Optional[float] = None

    def add_skill(self, skill):
        """
        Add a skill if it is not already present.
        """
        skill = skill.strip()

        if skill and skill.lower() not in {
            existing.lower() for existing in self.skills
        }:
            self.skills.append(skill)

    def add_career_interest(self, career):
        """
        Add a career interest if it is not already present.
        """
        career = career.strip()

        if career and career.lower() not in {
            existing.lower() for existing in self.career_interests
        }:
            self.career_interests.append(career)

    def update_resume(self, resume_text):
        """
        Store the extracted resume text.
        """
        self.resume_text = resume_text or ""

    def update_education(self, education):
        """
        Store the user's education information.
        """
        self.education = education or ""

    def update_experience(self, experience_years):
        """
        Store the user's years of experience.
        """
        self.experience_years = experience_years

    def get_profile_summary(self):
        """
        Return a simple summary of the user's profile.
        """
        return {
            "email": self.email,
            "name": self.name,
            "skills": self.skills,
            "career_interests": self.career_interests,
            "education": self.education,
            "experience_years": self.experience_years,
            "resume_available": bool(self.resume_text.strip()),
        }
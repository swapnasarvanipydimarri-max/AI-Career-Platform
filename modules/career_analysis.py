from dataclasses import dataclass, field
from typing import Dict, List, Optional


@dataclass
class CareerAnalysisResult:
    """
    Stores the results of a user's career analysis.
    """

    recommended_careers: List[str] = field(default_factory=list)
    predicted_careers: List[str] = field(default_factory=list)
    skill_gaps: List[str] = field(default_factory=list)
    job_skill_gaps: List[str] = field(default_factory=list)

    readiness_score: Optional[float] = None
    job_match_score: Optional[float] = None

    roadmap: List[str] = field(default_factory=list)
    courses: List[str] = field(default_factory=list)
    projects: List[str] = field(default_factory=list)

    def add_recommended_career(self, career):
        """
        Add a recommended career without duplicates.
        """
        career = career.strip()

        if career and career.lower() not in {
            item.lower() for item in self.recommended_careers
        }:
            self.recommended_careers.append(career)

    def add_skill_gap(self, skill):
        """
        Add a missing skill without duplicates.
        """
        skill = skill.strip()

        if skill and skill.lower() not in {
            item.lower() for item in self.skill_gaps
        }:
            self.skill_gaps.append(skill)

    def set_readiness_score(self, score):
        """
        Store the career readiness score.
        """
        self.readiness_score = float(score)

    def set_job_match_score(self, score):
        """
        Store the job matching score.
        """
        self.job_match_score = float(score)

    def get_summary(self) -> Dict:
        """
        Return the career analysis as a dictionary.
        """
        return {
            "recommended_careers": self.recommended_careers,
            "predicted_careers": self.predicted_careers,
            "skill_gaps": self.skill_gaps,
            "job_skill_gaps": self.job_skill_gaps,
            "readiness_score": self.readiness_score,
            "job_match_score": self.job_match_score,
            "roadmap": self.roadmap,
            "courses": self.courses,
            "projects": self.projects,
        }
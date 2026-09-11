from dataclasses import dataclass, field
from datetime import datetime
from typing import List

from modules.career_analysis import CareerAnalysisResult


@dataclass
class AnalysisRecord:
    """
    Represents one career analysis performed by a user.
    """

    timestamp: str
    result: CareerAnalysisResult


@dataclass
class AnalysisHistory:
    """
    Stores career analysis results for a user during the session.
    """

    records: List[AnalysisRecord] = field(default_factory=list)

    def add_analysis(self, result):
        """
        Add a new career analysis result.
        """
        if not isinstance(result, CareerAnalysisResult):
            raise TypeError(
                "result must be a CareerAnalysisResult instance."
            )

        record = AnalysisRecord(
            timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            result=result,
        )

        self.records.append(record)

    def get_latest(self):
        """
        Return the most recent analysis result.
        """
        if not self.records:
            return None

        return self.records[-1].result

    def get_analysis_count(self):
        """
        Return the number of stored analyses.
        """
        return len(self.records)

    def get_history_summary(self):
        """
        Return a summary of all stored analyses.
        """
        summary = []

        for record in self.records:
            summary.append(
                {
                    "timestamp": record.timestamp,
                    "readiness_score": record.result.readiness_score,
                    "job_match_score": record.result.job_match_score,
                    "recommended_careers": record.result.recommended_careers,
                    "skill_gaps": record.result.skill_gaps,
                }
            )

        return summary
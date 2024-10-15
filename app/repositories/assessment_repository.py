# app/repositories/assessment_repository.py

from typing import Dict, Optional
from ..models import AssessmentResultBase


class AssessmentRepository:
    def __init__(self) -> None:
        self.assessments: Dict[int, AssessmentResultBase] = {}
        self.next_id: int = 1

    def save(self, assessment: AssessmentResultBase) -> AssessmentResultBase:
        assessment.id = self.next_id
        self.assessments[self.next_id] = assessment
        self.next_id += 1
        return assessment

    def get(self, assessment_id: int) -> Optional[AssessmentResultBase]:
        return self.assessments.get(assessment_id)

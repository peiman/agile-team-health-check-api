# app/models.py

from typing import List, Dict
from pydantic import BaseModel
from datetime import datetime
from enum import Enum

class SurveyType(str, Enum):
    WEEKLY = "weekly"
    MONTHLY = "monthly"
    # Add more types as needed

class QuestionBase(BaseModel):
    id: int
    text: str
    scale_min: int
    scale_max: int
    reverse_scored: bool = False

class AnswerBase(BaseModel):
    question_id: int
    score: float  # Using float to accommodate different scales

class SurveyBase:
    def __init__(self, id: int, name: str, survey_type: SurveyType, questions: List[QuestionBase]):
        self.id = id
        self.name = name
        self.survey_type = survey_type
        self.questions = questions

class ResponseBase(BaseModel):
    survey_id: int
    answers: List[AnswerBase]
    timestamp: datetime

class AssessmentResultBase(BaseModel):
    id: int
    survey_id: int
    scores: Dict[str, float]
    timestamp: datetime

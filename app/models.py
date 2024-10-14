# app/models.py

from typing import List, Dict
from pydantic import BaseModel, Field
from datetime import datetime
from enum import Enum

class SurveyType(str, Enum):
    WEEKLY = "weekly"
    MONTHLY = "monthly"

class QuestionBase(BaseModel):
    id: int = Field(..., description="Unique identifier for the question")
    text: str = Field(..., description="The question text")
    scale_min: int = Field(..., description="Minimum value for the scale")
    scale_max: int = Field(..., description="Maximum value for the scale")
    reverse_scored: bool = Field(False, description="Indicates if the question is reverse-scored")

class AnswerBase(BaseModel):
    question_id: int = Field(..., description="ID of the question being answered")
    score: float = Field(..., description="Score given for the question")
class SurveyBase:
    """
    Represents a survey instrument with its associated questions and scoring mechanism.

    Attributes:
        id (int): Unique identifier for the survey.
        name (str): Name of the survey.
        survey_type (SurveyType): Type of the survey (e.g., weekly, monthly).
        questions (List[QuestionBase]): List of questions included in the survey.
    """

    def __init__(self, id: int, name: str, survey_type: SurveyType, questions: List[QuestionBase]):
        self.id = id
        self.name = name
        self.survey_type = survey_type
        self.questions = questions

class SurveyModel(BaseModel):
    """
    Pydantic model representing a survey, used for API responses.

    Attributes:
        id (int): Unique identifier for the survey.
        name (str): Name of the survey.
        survey_type (SurveyType): Type of the survey.
        questions (List[QuestionBase]): List of questions included in the survey.
    """
    id: int = Field(..., description="Unique identifier for the survey")
    name: str = Field(..., description="Name of the survey")
    survey_type: SurveyType = Field(..., description="Type of the survey")
    questions: List[QuestionBase] = Field(..., description="List of questions included in the survey")

class SurveySummary(BaseModel):
    """
    Pydantic model representing a summary of a survey.

    Attributes:
        id (int): Unique identifier for the survey.
        name (str): Name of the survey.
        survey_type (SurveyType): Type of the survey.
    """
    id: int = Field(..., description="Unique identifier for the survey")
    name: str = Field(..., description="Name of the survey")
    survey_type: SurveyType = Field(..., description="Type of the survey")

class ResponseBase(BaseModel):
    survey_id: int = Field(..., description="ID of the survey being responded to")
    answers: List[AnswerBase] = Field(..., description="List of answers")
    timestamp: datetime = Field(..., description="Timestamp of when the response was submitted")

class AssessmentResultBase(BaseModel):
    id: int = Field(..., description="Unique identifier for the assessment result")
    survey_id: int = Field(..., description="ID of the survey")
    scores: Dict[str, float] = Field(..., description="Calculated scores from the responses")
    timestamp: datetime = Field(..., description="Timestamp of when the assessment was created")

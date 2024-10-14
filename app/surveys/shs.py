# app/surveys/shs.py

from typing import List, Dict
from ..models import SurveyBase, QuestionBase, AnswerBase, SurveyType
from ..scoring import ScoringMechanism
import logging

logger = logging.getLogger(__name__)

class SHSScoringMechanism(ScoringMechanism):
    def calculate_score(self, answers: List[AnswerBase], questions: List[QuestionBase]) -> Dict[str, float]:
        total_score = 0
        for answer in answers:
            question = next((q for q in questions if q.id == answer.question_id), None)
            if not question:
                logger.warning(f"Question ID {answer.question_id} not found in SHS questions.")
                continue
            score = answer.score
            if question.reverse_scored:
                score = question.scale_max + question.scale_min - score
                logger.debug(f"Reverse-scored question {question.id}: original score {answer.score}, reversed score {score}")
            total_score += score
        average_score = total_score / len(questions)
        logger.info(f"Calculated happiness score: {average_score}")
        return {"happiness_score": round(average_score, 2)}

class SHSSurvey(SurveyBase):
    def __init__(self):
        super().__init__(
            id=1,
            name="Subjective Happiness Scale",
            survey_type=SurveyType.WEEKLY,
            questions=[
                QuestionBase(id=1, text="In general, I consider myself:", scale_min=1, scale_max=7),
                QuestionBase(id=2, text="Compared to most of my peers, I consider myself:", scale_min=1, scale_max=7),
                QuestionBase(id=3, text="Some people are generally very happy...", scale_min=1, scale_max=7),
                QuestionBase(id=4, text="Some people are generally not very happy...", scale_min=1, scale_max=7, reverse_scored=True),
            ]
        )
        self.scoring_mechanism = SHSScoringMechanism()

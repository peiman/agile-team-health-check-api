# app/surveys/stress.py

from typing import List, Dict
from ..models import SurveyBase, QuestionBase, AnswerBase, SurveyType
from ..scoring import ScoringMechanism
import logging

logger = logging.getLogger(__name__)


class StressScoringMechanism(ScoringMechanism):
    def calculate_score(
        self, answers: List[AnswerBase], questions: List[QuestionBase]
    ) -> Dict[str, float]:
        # Assuming only one answer for the stress question
        stress_score = answers[0].score
        logger.info(f"Calculated stress score: {stress_score}")
        return {"stress_score": stress_score}


class StressSurvey(SurveyBase):
    def __init__(self) -> None:
        scoring_mechanism = StressScoringMechanism()
        super().__init__(
            id=2,
            name="Single-Item Stress Measure",
            survey_type=SurveyType.WEEKLY,
            questions=[
                QuestionBase(
                    id=5,
                    text="On a scale from 1 to 5, how stressed have you felt this week?",  # noqa
                    scale_min=1,
                    scale_max=5,
                    reverse_scored=False,
                ),
            ],
            scoring_mechanism=scoring_mechanism,
        )
        self.scoring_mechanism = StressScoringMechanism()

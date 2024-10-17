# app/surveys/shs.py

from typing import List, Dict
from ..models import SurveyBase, QuestionBase, AnswerBase, SurveyType
from ..scoring import ScoringMechanism
import logging

logger = logging.getLogger(__name__)


class SHSConstants:
    HIGH = (
        "High Subjective Happiness: "
        "Individuals perceive themselves as very happy, "
        "with strong positive self-assessment and "
        "alignment with positive happiness characteristics."
    )

    MODERATE = (
        "Moderate Subjective Happiness: "
        "Individuals experience a moderate level of happiness, "
        "with a balanced self-assessment and "
        "some alignment with positive happiness traits."
    )

    LOW = (
        "Low Subjective Happiness: "
        "Individuals perceive themselves as less happy, "
        "with negative self-assessment and "
        "strong alignment with negative happiness descriptions."
    )

    INTERPRETATION_GUIDE = """
    Interpreting the Subjective Happiness Scale (SHS) scores involves understanding the range and meaning of the average score derived from the four survey items.

    Scoring Overview:
    - Number of Items: 4
    - Response Scale: Each item is rated on a 7-point scale (1: Strongly disagree / Not at all, 7: Strongly agree / A great deal)
    - Item 4 is reverse-scored
    - Calculate the average of all four items
    - Possible Range: 1 (lowest happiness) to 7 (highest happiness)

    Interpreting the Average Score:
    - 6 to 7: High Subjective Happiness
    - 4 to 5: Moderate Subjective Happiness
    - 1 to 3: Low Subjective Happiness

    Considerations for Interpretation:
    - Consider contextual factors, cultural sensitivity, and use a holistic assessment approach.
    """  # noqa: E501


def get_shs_interpretation(score: float) -> str:
    if 6 <= score <= 7:
        return SHSConstants.HIGH
    elif 4 <= score < 6:
        return SHSConstants.MODERATE
    else:
        return SHSConstants.LOW


class SHSScoringMechanism(ScoringMechanism):
    def calculate_score(
        self, answers: List[AnswerBase], questions: List[QuestionBase]
    ) -> Dict[str, float]:
        total_score = 0.0
        for answer in answers:
            question = next((q for q in questions if q.id == answer.question_id), None)
            if not question:
                logger.warning(
                    f"Question ID {answer.question_id} not found in SHS questions."
                )
                continue
            score = answer.score
            if question.reverse_scored:
                score = question.scale_max + question.scale_min - score
                logger.debug(
                    f"Reverse-scored question {question.id}: "
                    f"original score {answer.score}, reversed score {score}"
                )
            total_score += score
        average_score = total_score / len(questions)
        interpretation = get_shs_interpretation(average_score)
        logger.info(f"Subjective Happiness Scale (SHS) Score: {average_score:.2f}")
        logger.info(f"SHS Interpretation: {interpretation}")
        return {"happiness_score": round(average_score, 2)}


class SHSSurvey(SurveyBase):
    def __init__(self) -> None:
        scoring_mechanism = SHSScoringMechanism()
        super().__init__(
            id=1,
            name="Subjective Happiness Scale",
            survey_type=SurveyType.WEEKLY,
            questions=[
                QuestionBase(
                    id=1,
                    text="In general, I consider myself...",
                    scale_min=1,
                    scale_max=7,
                    scale_min_label="not a very happy person",
                    scale_max_label="a very happy person",
                    reverse_scored=False,
                ),
                QuestionBase(
                    id=2,
                    text="Compared to most of my peers, I consider myself...",
                    scale_min=1,
                    scale_max=7,
                    scale_min_label="less happy",
                    scale_max_label="more happy",
                    reverse_scored=False,
                ),
                QuestionBase(
                    id=3,
                    text=(
                        "Some people are generally very happy. "
                        "They enjoy life regardless of what is going on, "
                        "getting the most out of everything. "
                        "To what extent does this characterization describe you?"
                    ),
                    scale_min=1,
                    scale_max=7,
                    scale_min_label="not at all",
                    scale_max_label="a great deal",
                    reverse_scored=False,
                ),
                QuestionBase(
                    id=4,
                    text=(
                        "Some people are generally not very happy. "
                        "Although they are not depressed, "
                        "they never seem as happy as they might be. "
                        "To what extent does this characterization describe you?"
                    ),
                    scale_min=1,
                    scale_max=7,
                    scale_min_label="a great deal",
                    scale_max_label="not at all",
                    reverse_scored=True,
                ),
            ],
            scoring_mechanism=scoring_mechanism,
        )
        self.interpretation_guide = SHSConstants.INTERPRETATION_GUIDE

    def get_interpretation(self, score: float) -> str:
        return get_shs_interpretation(score)

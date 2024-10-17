# app/surveys/stress.py

from typing import List, Dict
from ..models import SurveyBase, QuestionBase, AnswerBase, SurveyType
from ..scoring import ScoringMechanism
import logging

logger = logging.getLogger(__name__)


class StressConstants:
    NOT_AT_ALL = (
        "Not at All Stressed: The individual did not experience any "
        "noticeable stress during the week. "
        "This indicates high levels of relaxation and calmness, "
        "effective coping mechanisms, and potentially "
        "high life satisfaction and well-being."
    )

    SLIGHTLY = (
        "Slightly Stressed: The individual felt minor stressors "
        "but managed them effectively without significant impact. "
        "Minor challenges were present but easily handled, "
        "with a general sense of well-being and only occasional stress."
    )

    MODERATELY = (
        "Moderately Stressed: The individual experienced a "
        "moderate level of stress that may have impacted their "
        "daily life to some extent. There were noticeable "
        "stressors that require attention, with possible "
        "impacts on mood, energy levels, or productivity."
    )

    VERY = (
        "Very Stressed: The individual felt a "
        "high level of stress that likely affected "
        "various aspects of their life. "
        "Significant challenges or pressures were experienced, "
        "with potential negative effects on mental and physical health."
    )

    EXTREMELY = (
        "Extremely Stressed: The individual experienced "
        "overwhelming stress that severely "
        "impacted their well-being. This indicates "
        "intense stressors possibly leading to "
        "burnout or mental health issues, with an urgent "
        "need for support or professional help."
    )

    INVALID = "Invalid stress score. Please provide a score between 1 and 5."

    INTERPRETATION_GUIDE = """
    Interpreting the Single-Item Stress Measure involves understanding the respondent's perceived stress level within the specified timeframe—in this case, weekly.

    Stress Measure Overview:
    Question: "On a scale from 1 to 5, how stressed have you felt this week?"
    Response Scale:
    1: Not at all stressed
    2: Slightly stressed
    3: Moderately stressed
    4: Very stressed
    5: Extremely stressed

    Considerations for Interpretation:
    - Responses are subjective and can be influenced by current mood, recent events, or individual perception of stress.
    - Consider contextual factors such as major life changes, work deadlines, or personal issues.
    - Cultural backgrounds may influence how individuals perceive and report stress.
    - Consider complementing with additional measures for a more comprehensive understanding.
    """  # noqa: E501


def get_stress_interpretation(score: int) -> str:
    interpretations = {
        1: StressConstants.NOT_AT_ALL,
        2: StressConstants.SLIGHTLY,
        3: StressConstants.MODERATELY,
        4: StressConstants.VERY,
        5: StressConstants.EXTREMELY,
    }
    return interpretations.get(score, StressConstants.INVALID)


class StressScoringMechanism(ScoringMechanism):
    def calculate_score(
        self, answers: List[AnswerBase], questions: List[QuestionBase]
    ) -> Dict[str, float]:
        # Assuming only one answer for the stress question
        stress_score = answers[0].score
        interpretation = get_stress_interpretation(int(stress_score))
        logger.info(f"Single-Item Stress Measure Score: {stress_score}")
        logger.info(f"Stress Interpretation: {interpretation}")
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
                    text=(
                        "On a scale from 1 to 5, "
                        "how stressed have you felt this week?"
                    ),
                    scale_min=1,
                    scale_max=5,
                    scale_min_label="Not at all stressed",
                    scale_max_label="Extremely stressed",
                    reverse_scored=False,
                ),
            ],
            scoring_mechanism=scoring_mechanism,
        )
        self.interpretation_guide = StressConstants.INTERPRETATION_GUIDE

    def get_interpretation(self, score: float) -> str:
        return get_stress_interpretation(int(score))

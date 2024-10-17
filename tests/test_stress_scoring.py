# tests/test_stress_scoring.py

import pytest
from pytest_assume.plugin import assume
from app.surveys.stress import StressSurvey, get_stress_interpretation, StressConstants
from app.models import AnswerBase


@pytest.fixture
def stress_survey() -> StressSurvey:
    return StressSurvey()


def test_stress_scoring_valid_input(stress_survey: StressSurvey) -> None:
    answers = [AnswerBase(question_id=5, score=3)]
    scores = stress_survey.scoring_mechanism.calculate_score(
        answers, stress_survey.questions
    )
    assume(scores["stress_score"] == 3)


def test_stress_interpretation() -> None:
    assume(get_stress_interpretation(1) == StressConstants.NOT_AT_ALL)
    assume(get_stress_interpretation(2) == StressConstants.SLIGHTLY)
    assume(get_stress_interpretation(3) == StressConstants.MODERATELY)
    assume(get_stress_interpretation(4) == StressConstants.VERY)
    assume(get_stress_interpretation(5) == StressConstants.EXTREMELY)
    assume(get_stress_interpretation(6) == StressConstants.INVALID)


def test_stress_survey_get_interpretation(stress_survey: StressSurvey) -> None:
    assume(stress_survey.get_interpretation(1) == StressConstants.NOT_AT_ALL)
    assume(stress_survey.get_interpretation(3) == StressConstants.MODERATELY)
    assume(stress_survey.get_interpretation(5) == StressConstants.EXTREMELY)


def test_stress_survey_interpretation_guide(stress_survey: StressSurvey) -> None:
    assume(stress_survey.interpretation_guide is not None)
    assume(
        "Interpreting the Single-Item Stress Measure"
        in stress_survey.interpretation_guide
    )

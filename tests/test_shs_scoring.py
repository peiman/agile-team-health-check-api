# tests/test_shs_scoring.py

import pytest
from pytest_assume.plugin import assume
from app.surveys.shs import SHSSurvey, get_shs_interpretation, SHSConstants
from app.models import AnswerBase


@pytest.fixture
def shs_survey() -> SHSSurvey:
    return SHSSurvey()


def test_shs_scoring_valid_input(shs_survey: SHSSurvey) -> None:
    answers = [
        AnswerBase(question_id=1, score=5),
        AnswerBase(question_id=2, score=6),
        AnswerBase(question_id=3, score=4),
        AnswerBase(question_id=4, score=2),
    ]
    scores = shs_survey.scoring_mechanism.calculate_score(answers, shs_survey.questions)
    assume(scores["happiness_score"] == 5.25)


def test_shs_scoring_reverse_item(shs_survey: SHSSurvey) -> None:
    answers = [
        AnswerBase(question_id=4, score=2),  # Reverse-scored
    ]
    question = next(q for q in shs_survey.questions if q.id == 4)
    score = answers[0].score
    if question.reverse_scored:
        score = question.scale_max + question.scale_min - score
    assume(score == 6)  # Reverse of 2 on a scale of 1-7 is 6


def test_shs_interpretation() -> None:
    assume(get_shs_interpretation(6.5) == SHSConstants.HIGH)
    assume(get_shs_interpretation(4.5) == SHSConstants.MODERATE)
    assume(get_shs_interpretation(2.5) == SHSConstants.LOW)


def test_shs_survey_get_interpretation(shs_survey: SHSSurvey) -> None:
    assume(shs_survey.get_interpretation(6.5) == SHSConstants.HIGH)
    assume(shs_survey.get_interpretation(4.5) == SHSConstants.MODERATE)
    assume(shs_survey.get_interpretation(2.5) == SHSConstants.LOW)


def test_shs_survey_interpretation_guide(shs_survey: SHSSurvey) -> None:
    assume(shs_survey.interpretation_guide is not None)
    assume(
        "Interpreting the Subjective Happiness Scale (SHS)"
        in shs_survey.interpretation_guide
    )

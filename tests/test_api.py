# tests/test_api.py
import pytest
from pytest_assume.plugin import assume
from fastapi.testclient import TestClient
from app.main import app
from app.survey_registry import survey_registry

client = TestClient(app)


def test_root_endpoint() -> None:
    response = client.get("/")
    assume(response.status_code == 200)
    assume(response.json()["message"] == "Welcome to the Agile Team Health Check API")
    assume("version" in response.json())
    assume("api_version" in response.json())
    assume("docs_url" in response.json())


def test_list_surveys() -> None:
    response = client.get("/v1/surveys/")
    assume(response.status_code == 200)
    data = response.json()
    assume(isinstance(data, list))

    # Get expected surveys from the SurveyRegistry
    expected_surveys = survey_registry.list_surveys()
    assume(len(data) == len(expected_surveys))

    # Map response data by survey ID for easy lookup
    response_surveys = {survey["id"]: survey for survey in data}

    for expected_survey in expected_surveys:
        survey_id = expected_survey.id
        assume(survey_id in response_surveys)
        response_survey = response_surveys[survey_id]
        assume(response_survey["name"] == expected_survey.name)
        assume(response_survey["survey_type"] == expected_survey.survey_type.value)


def test_get_survey_details() -> None:
    # Get a survey ID from the SurveyRegistry
    survey_ids = [survey.id for survey in survey_registry.list_surveys()]
    survey_id = survey_ids[0]  # Test with the first survey

    response = client.get(f"/v1/surveys/{survey_id}")
    assume(response.status_code == 200)
    data = response.json()
    expected_survey = survey_registry.get_survey(survey_id)

    if expected_survey is None:
        pytest.fail(f"Survey with ID {survey_id} should not be None")

    assume(data["id"] == expected_survey.id)
    assume(data["name"] == expected_survey.name)
    assume(data["survey_type"] == expected_survey.survey_type.value)
    assume(len(data["questions"]) == len(expected_survey.questions))


def test_get_survey_questions() -> None:
    # Get a survey ID from the SurveyRegistry
    survey_ids = [survey.id for survey in survey_registry.list_surveys()]
    survey_id = survey_ids[0]  # Test with the first survey

    response = client.get(f"/v1/surveys/{survey_id}/questions")
    assume(response.status_code == 200)
    data = response.json()
    expected_survey = survey_registry.get_survey(survey_id)

    if expected_survey is None:
        pytest.fail(f"Survey with ID {survey_id} should not be None")

    assume(len(data) == len(expected_survey.questions))
    for question in data:
        assume("id" in question)
        assume("text" in question)
        assume("scale_min" in question)
        assume("scale_max" in question)


def test_submit_survey_response_valid() -> None:
    # Get a survey from the SurveyRegistry
    expected_survey = survey_registry.get_survey(1)

    if expected_survey is None:
        pytest.fail("Survey with ID 1 should not be None")

    survey_id = expected_survey.id
    # Prepare answers with valid scores within the scale
    answers = []
    for question in expected_survey.questions:
        score = (question.scale_min + question.scale_max) / 2  # Middle of the scale
        answers.append({"question_id": question.id, "score": score})
    response = client.post(
        f"/v1/surveys/{survey_id}/responses",
        json={
            "survey_id": survey_id,
            "answers": answers,
            "timestamp": "2023-10-14T12:00:00Z",
        },
    )
    assume(response.status_code == 200)
    data = response.json()
    assume("scores" in data)


def test_submit_survey_response_missing_answer() -> None:
    # Get a survey from the SurveyRegistry
    expected_survey = survey_registry.get_survey(1)

    if expected_survey is None:
        pytest.fail("Survey with ID 1 should not be None")

    survey_id = expected_survey.id
    # Prepare answers but omit one question
    answers = []
    for question in expected_survey.questions[:-1]:  # Omit the last question
        score = (question.scale_min + question.scale_max) / 2
        answers.append({"question_id": question.id, "score": score})
    response = client.post(
        f"/v1/surveys/{survey_id}/responses",
        json={
            "survey_id": survey_id,
            "answers": answers,
            "timestamp": "2023-10-14T12:00:00Z",
        },
    )
    assume(response.status_code == 400)
    assume("Incomplete set of answers" in response.json()["detail"])


def test_submit_survey_response_invalid_score() -> None:
    # Get a survey from the SurveyRegistry
    expected_survey = survey_registry.get_survey(1)

    if expected_survey is None:
        pytest.fail("Survey with ID 1 should not be None")

    survey_id = expected_survey.id
    # Prepare answers with an invalid score
    answers = []
    for question in expected_survey.questions:
        score = question.scale_max + 1  # Invalid score
        answers.append({"question_id": question.id, "score": score})
    response = client.post(
        f"/v1/surveys/{survey_id}/responses",
        json={
            "survey_id": survey_id,
            "answers": answers,
            "timestamp": "2023-10-14T12:00:00Z",
        },
    )
    assume(response.status_code == 400)
    assume("must be between" in response.json()["detail"])

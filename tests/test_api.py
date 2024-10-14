# tests/test_api.py

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_get_survey_questions():
    response = client.get("/surveys/1/questions")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 4  # SHS has 4 questions


def test_submit_shs_response_valid():
    response = client.post(
        "/surveys/1/responses",
        json={
            "survey_id": 1,
            "answers": [
                {"question_id": 1, "score": 5},
                {"question_id": 2, "score": 6},
                {"question_id": 3, "score": 4},
                {"question_id": 4, "score": 2},
            ],
            "timestamp": "2023-10-14T12:00:00Z"
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data["scores"]["happiness_score"] == 5.25


def test_submit_shs_response_missing_answer():
    response = client.post(
        "/surveys/1/responses",
        json={
            "survey_id": 1,
            "answers": [
                {"question_id": 1, "score": 5},
                # Missing other questions
            ],
            "timestamp": "2023-10-14T12:00:00Z"
        },
    )
    assert response.status_code == 400
    assert "Incomplete set of answers" in response.json()["detail"]


def test_submit_shs_response_invalid_score():
    response = client.post(
        "/surveys/1/responses",
        json={
            "survey_id": 1,
            "answers": [
                {"question_id": 1, "score": 8},  # Invalid score
                {"question_id": 2, "score": 6},
                {"question_id": 3, "score": 4},
                {"question_id": 4, "score": 2},
            ],
            "timestamp": "2023-10-14T12:00:00Z"
        },
    )
    assert response.status_code == 400
    assert "must be between" in response.json()["detail"]

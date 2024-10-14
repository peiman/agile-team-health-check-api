# tests/test_main.py

from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_get_questions():
    response = client.get("/questions")
    assert response.status_code == 200
    assert len(response.json()) > 0

def test_submit_response():
    response = client.post(
        "/responses",
        json=[
            {"question_id": 1, "score": 4},
            {"question_id": 2, "score": 5}
        ]
    )
    assert response.status_code == 201
    assert response.json()["id"] == 1

def test_get_response():
    response = client.get("/responses/1")
    assert response.status_code == 200
    assert response.json()["id"] == 1

def test_get_nonexistent_response():
    response = client.get("/responses/999")
    assert response.status_code == 404

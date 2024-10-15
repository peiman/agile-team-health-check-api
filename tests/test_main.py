# tests/test_main.py

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_root_endpoint() -> None:
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello agile team"}

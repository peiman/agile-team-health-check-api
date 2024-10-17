# tests/test_main.py

from pytest_assume.plugin import assume
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_root_endpoint() -> None:
    response = client.get("/")
    assume(response.status_code == 200)
    assume(response.json() == {"message": "Hello agile team"})

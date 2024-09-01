import pytest
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_home():
    response = client.get("/")
    assert response.status_code == 200


def test_dashboard():
    response = client.get("/dashboard")
    assert response.status_code == 403
    assert response.json() == {"detail": "Invalid session."}


def test_main():
    response = client.post("/", data={"username": "keejan", "manga": "on"})
    assert response.status_code == 200
    response = client.get("/dashboard")
    assert response.status_code == 200

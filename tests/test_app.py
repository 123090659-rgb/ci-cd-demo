"""Tests for the CI/CD demo app."""

from app import add, app


def test_add():
    assert add(2, 3) == 5
    assert add(-1, 1) == 0


def test_index():
    client = app.test_client()
    response = client.get("/")
    assert response.status_code == 200
    assert response.get_json()["message"] == "Hello from the CI/CD demo app!"


def test_add_endpoint():
    client = app.test_client()
    response = client.get("/add/2/3.5")
    assert response.status_code == 200
    assert response.get_json()["result"] == 5.5


def test_health():
    client = app.test_client()
    response = client.get("/health")
    assert response.status_code == 200
    assert response.get_json()["status"] == "ok"

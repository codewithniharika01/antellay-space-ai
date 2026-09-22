import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["api_version"] == "v1"


def test_get_satellites():
    response = client.get("/api/v1/satellites")
    assert response.status_code == 200


def test_get_missing_satellite():
    response = client.get("/api/v1/satellites/999999")
    assert response.status_code == 404


def test_validation_error():
    response = client.post(
        "/api/v1/auth/register",
        json={
            "username": "test_user"
        }
    )

    assert response.status_code == 422

    data = response.json()

    assert data["success"] is False
    assert data["error"]["code"] == "VALIDATION_ERROR"
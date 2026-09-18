import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_get_satellites():
    response = client.get("/satellites")
    assert response.status_code == 200


def test_get_missing_satellite():
    response = client.get("/satellites/999999")
    assert response.status_code == 404
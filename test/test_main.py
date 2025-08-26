import pytest
from fastapi.testclient import TestClient
from src.main import app


def verify_response(response, expected_status, expected_json):
    assert response.status_code == expected_status
    assert response.json() == expected_json

@pytest.mark.asyncio
async def test_health_check():
    client = TestClient(app=app)
    response = client.get("/health")
    verify_response(response, 200, {"status": "ok"})


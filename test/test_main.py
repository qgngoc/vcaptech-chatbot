import pytest
from httpx import AsyncClient
from src.main import app


def verify_response(response, expected_status, expected_json):
    assert response.status_code == expected_status
    assert response.json() == expected_json

@pytest.mark.asyncio
async def test_read_root():
    async with AsyncClient(app=app) as ac:
        response = await ac.get("/health")
    assert verify_response(response, 200, {"status": "ok"})


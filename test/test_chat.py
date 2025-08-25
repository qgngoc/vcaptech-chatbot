import pytest
from httpx import AsyncClient
from src.main import app



@pytest.mark.asyncio
async def test_chat_1():
    
    def verify_response(response):
        assert response.status_code == 200
        output_text = response.json().get("answer", "").lower()
        assert output_text
    
    async with AsyncClient(app=app) as ac:
        input_data = {
            "messages": [
                {"role": "user", "content": "Hello"}
            ],
            "client": "0",
            "rag_config": {
                "llm_config": {
                    "model": "gpt-4.1-mini",
                    "base_url": "http://localhost:8000/v1"
                },
                "top_k": 5,
            }
        }
        response = await ac.post("/api/v1/chat", json=input_data)
        assert verify_response(response)



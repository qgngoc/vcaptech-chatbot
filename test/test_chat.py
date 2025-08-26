
import pytest
from fastapi.testclient import TestClient
from src.main import app


@pytest.mark.asyncio
async def test_chat_1():
    
    def verify_response(response):
        assert response.status_code == 200
        output_text = response.json().get("answer", "").lower()
        assert output_text

    client = TestClient(app=app)
    input_data = {
        "messages": [
            {"role": "user", "content": "Hello"}
        ],
        "client": {
                "id": "0"
            },
            "rag_config": {
                "llm_config": {
                    "model_path": "gpt-4.1-mini"
                },
                "top_k": 5
            }
        }
    response = client.post("/api/v1/chat", json=input_data)
    verify_response(response)


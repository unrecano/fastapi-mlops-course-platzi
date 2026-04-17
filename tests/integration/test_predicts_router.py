import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_predicts_success(app_client: AsyncClient):
    payload = {
        "sentences": [
            {"client_name": "Alice", "text": "This is a test sentence for the bank"}
        ]
    }

    response = await app_client.post("/predicts", json=payload)

    assert response.status_code == 200
    data = response.json()
    assert "predictions" in data
    assert len(data["predictions"]) == 1
    assert data["predictions"][0]["client_name"] == "Alice"
    assert (
        data["predictions"][0]["prediction"] == "Bank Account Services"
    )  # Because mock model returns 0


@pytest.mark.asyncio
async def test_predicts_validation_error(app_client: AsyncClient):
    # Invalid payload (missing sentences field)
    payload = {"wrong_field": [{"client_name": "Bob", "text": "Text"}]}

    response = await app_client.post("/predicts", json=payload)

    # FastAPI Pydantic should return 422 Unprocessable Entity
    assert response.status_code == 422

import pytest


@pytest.mark.asyncio
async def test_healthcheck_endpoint(app_client):
    response = await app_client.get("/healthcheck")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


@pytest.mark.asyncio
async def test_root_endpoint(app_client):
    response = await app_client.get("/")
    assert response.status_code == 200
    assert response.json() == {"Hello": "World"}

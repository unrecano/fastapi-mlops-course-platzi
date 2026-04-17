import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from typing import AsyncGenerator
from unittest.mock import AsyncMock

from app.main import app
from app.db.engine import get_session


# Mock para el modelo de ML y CountVectorizer
class MockModel:
    def predict(self, X):
        return [0] * len(X)  # Retorna una lista con la categoría "0"


from scipy.sparse import csr_matrix
import numpy as np


class MockVectorizer:
    def transform(self, X):
        return csr_matrix(np.array([[0.1, 0.2]]))


@pytest_asyncio.fixture(autouse=True)
async def lifespan_overrides():
    """Mockea las variables de estado que normalmente carga el lifespan."""
    app.state.model = MockModel()
    app.state.count_vectorizer = MockVectorizer()
    yield
    app.state.model = None
    app.state.count_vectorizer = None


async def override_get_session() -> AsyncGenerator[AsyncMock, None]:
    """Mock asíncrono para evitar conexión a PostgreSQL."""
    mock_session = AsyncMock()
    yield mock_session


app.dependency_overrides[get_session] = override_get_session


@pytest_asyncio.fixture
async def app_client() -> AsyncGenerator[AsyncClient, None]:
    """Cliente asíncrono para probar endpoints de FastAPI."""
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        yield client

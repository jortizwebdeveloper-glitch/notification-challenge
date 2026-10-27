import pytest
from httpx import ASGITransport, AsyncClient

from main import app
from src.shared.settings import settings


@pytest.fixture
async def client():
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test",
    ) as ac:
        yield ac


@pytest.fixture(autouse=True)
def jwt_secret(monkeypatch):
    monkeypatch.setattr(
        settings, "SECRET_KEY_JWT", "secret_jwt_secret_jwt_secret_jwt_secret_jwt"
    )

import pytest
from httpx import ASGITransport, AsyncClient

from main import app
from src.shared.settings import settings

from sqlalchemy import create_engine, event
from sqlalchemy.orm import Session

from src.core.db import Base

# Importar los modelos es obligatorio: así se registran en Base.metadata
from src.modules.auth.infra.auth_model import AuthModel  # noqa: F401
from src.modules.users.infra.user_model import UserModel  # noqa: F401

from testcontainers.community.postgres import PostgresContainer
from alembic import command
from alembic.config import Config


@pytest.fixture(scope="session")
def postgres_url():
    with PostgresContainer("postgres:16", driver="psycopg") as pg:
        yield pg.get_connection_url()


@pytest.fixture
def engine(postgres_url):
    alembic_cfg = Config("alembic.ini")
    alembic_cfg.set_main_option("sqlalchemy.url", postgres_url)
    command.upgrade(alembic_cfg, "head")

    engine = create_engine(postgres_url)  # en memoria

    yield engine
    engine.dispose()


@pytest.fixture
def session(engine):
    with Session(engine) as session:
        yield session


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

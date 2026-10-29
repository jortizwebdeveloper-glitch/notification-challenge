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



@pytest.fixture
def engine():
    engine = create_engine("sqlite://")  # en memoria

    # SQLite no aplica llaves foráneas por defecto
    @event.listens_for(engine, "connect")
    def _enable_fk(dbapi_connection, _):
        dbapi_connection.execute("PRAGMA foreign_keys=ON")

    Base.metadata.create_all(engine)
    yield engine
    Base.metadata.drop_all(engine)
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


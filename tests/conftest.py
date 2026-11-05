from contextlib import asynccontextmanager

import pytest
import pytest_asyncio
from alembic import command
from alembic.config import Config
from arq import create_pool
from arq.connections import RedisSettings
from arq.worker import Worker
from httpx import ASGITransport, AsyncClient
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import Session
from testcontainers.community.postgres import PostgresContainer
from testcontainers.community.redis import RedisContainer

# Importar los modelos es obligatorio: así se registran en Base.metadata
import src.core.db.models  # noqa: F401
from main import app
from src.core.arq import get_arq
from src.core.db import get_async_session, get_session
from src.shared.settings import settings
from src.shared.workers.worker import WorkerSettings


@pytest.fixture(scope="session")
def postgres_url():
    with PostgresContainer("postgres:16", driver="psycopg") as pg:
        url = pg.get_connection_url()
        alembic_cfg = Config("alembic.ini")
        alembic_cfg.set_main_option("sqlalchemy.url", url)
        command.upgrade(alembic_cfg, "head")
        yield url


@pytest.fixture
def engine(postgres_url):
    engine = create_engine(postgres_url)  # en memoria
    yield engine
    engine.dispose()


@pytest.fixture
def session(engine):
    with Session(engine) as session:
        yield session


@pytest_asyncio.fixture
async def async_engine(postgres_url):
    engine = create_async_engine(postgres_url)
    yield engine
    await engine.dispose()


@pytest_asyncio.fixture
async def async_session_marker(async_engine):
    return async_sessionmaker(async_engine, expire_on_commit=False)


@pytest_asyncio.fixture
async def scope_async_session(async_session_marker):
    @asynccontextmanager
    async def scope():
        async with async_session_marker() as session:
            yield session

    return scope


@pytest_asyncio.fixture
async def async_session(scope_async_session):
    async with scope_async_session() as session:
        yield session


@pytest_asyncio.fixture(autouse=True)
def ptach_worker(monkeypatch, scope_async_session):

    # monkeypatch.setattr("src.core.db.async_engine", async_session)
    monkeypatch.setattr(
        "src.shared.workers.worker.scope_async_session", scope_async_session
    )


@pytest.fixture(scope="session")
def redis_container():
    with RedisContainer("redis:7-alpine") as container:
        yield container


@pytest.fixture(scope="session")
def redis_settings(redis_container) -> RedisSettings:
    return RedisSettings(
        host=redis_container.get_container_host_ip(),
        port=int(redis_container.get_exposed_port(6379)),
        database=0,
        password=None,
    )


@pytest_asyncio.fixture
async def arq_redis(redis_settings):
    pool = await create_pool(redis_settings)
    await pool.flushdb()  # cola limpia por test
    yield pool
    await pool.flushdb()
    await pool.aclose()


@pytest_asyncio.fixture
async def worker(arq_redis):
    w = Worker(
        functions=WorkerSettings.functions,
        redis_pool=arq_redis,
        burst=True,
        poll_delay=0,
        # on_startup=WorkerSettings.on_startup,
        # on_shutdown=WorkerSettings.on_shutdown,
    )

    yield w
    await w.close()


@pytest.fixture
async def client(arq_redis, session, async_session):
    app.dependency_overrides[get_arq] = lambda: arq_redis
    app.dependency_overrides[get_session] = lambda: session
    app.dependency_overrides[get_async_session] = lambda: async_session
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

from contextlib import asynccontextmanager

from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from src.shared.settings import settings


class Base(DeclarativeBase):
    pass


engine = create_engine(settings.DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

async_engine = create_async_engine(settings.ASYNC_DATABASE_URL)
AsyncSessionLocal = async_sessionmaker(bind=async_engine, expire_on_commit=False)


def get_session():
    with SessionLocal() as session:
        yield session


@asynccontextmanager
async def scope_async_session():
    async with AsyncSessionLocal() as session:
        yield session


async def get_async_session():
    async with scope_async_session() as session:
        yield session

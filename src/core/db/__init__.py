from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from src.shared.settings import settings


class Base(DeclarativeBase):
    pass


engine = create_engine(settings.DATABASE_URL)

SessionLocal = sessionmaker(bind=engine)


def get_session():
    with SessionLocal() as session:
        yield session

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.shared.settings import settings

engine = create_engine(settings.DATABASE_URL)

SessionLocal = sessionmaker(bind=engine)


def get_session():
    with SessionLocal as session:
        yield session

from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from contextlib import contextmanager


@contextmanager
def transaction_db(session: Session):
    try:
        yield
    except SQLAlchemyError:
        session.rollback()

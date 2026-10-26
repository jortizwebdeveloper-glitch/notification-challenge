from sqlalchemy.orm import Session
from contextlib import contextmanager


@contextmanager
def transaction_db(session: Session):
    try:
        yield
    except Exception as e:
        print(type(e), e)
        session.rollback()

from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from contextlib import contextmanager

from src.shared.errors.exceptions import InfrastructureError


@contextmanager
def transaction_db(session: Session):
    try:
        yield

    except SQLAlchemyError as exc:
        session.rollback()
        raise InfrastructureError("Error en la DB") from exc
    except Exception:
        session.rollback()
        raise

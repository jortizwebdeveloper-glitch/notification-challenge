from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from contextlib import contextmanager

from src.shared.errors.exceptions import AlreadyExistsError

UNIQUE_EMAIL = "ix_users_email"


def violated_constraint(exc: IntegrityError) -> str | None:
    diag = getattr(exc.orig, "diag", None)

    return getattr(diag, "constraint_name", None)


@contextmanager
def user_db_errors():
    try:
        yield
    except IntegrityError as exc:
        if violated_constraint(exc) == UNIQUE_EMAIL:
            raise AlreadyExistsError("Email ya registrado") from exc
        raise

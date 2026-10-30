import uuid
from contextlib import contextmanager
from datetime import UTC, datetime, timedelta
from typing import TypedDict

import jwt
from src.shared.errors.exceptions import ForbiddenError
from src.shared.settings import settings

ALGORITHM = "HS256"


class TokenPayload(TypedDict):
    sub: str
    iat: datetime
    exp: datetime
    jti: str


def create_token_jwt(sub: str):
    now = datetime.now(UTC)
    delta = now + timedelta(minutes=60)

    payload: TokenPayload = {
        "sub": sub,
        "iat": now,
        "exp": delta,
        "jti": str(uuid.uuid4()),
    }

    return jwt.encode(payload, settings.SECRET_KEY_JWT, algorithm=ALGORITHM)


def verify_token_jwt(token: str) -> TokenPayload:
    return jwt.decode(token, settings.SECRET_KEY_JWT, algorithms=ALGORITHM)


@contextmanager
def jwt_error_handle():
    try:
        yield
    except jwt.exceptions.PyJWTError as exc:
        raise ForbiddenError("Sin autorización") from exc

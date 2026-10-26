import jwt
import uuid

from src.shared.settings import settings
from datetime import datetime, timedelta, timezone
from contextlib import contextmanager

from src.shared.errors.exceptions import ForbiddenError

SECRET = settings.SECRET_KET_JWT
ALGORITHM = "HS256"


def create_token_jwt(sub: str):
    now = datetime.now(timezone.utc)
    delta = now + timedelta(minutes=15)

    payload = {
        "sub": sub,
        "iat": now,
        "exp": delta,
        "jti": str(uuid.uuid4()),
    }

    return jwt.encode(payload, SECRET, algorithm=ALGORITHM)


def verify_token_jwt(token: str):
    return jwt.decode(token, SECRET, algorithms=ALGORITHM)


@contextmanager
def jwt_error_handle():
    try:
        yield
    except jwt.exceptions.ExpiredSignatureError as exc:
        raise ForbiddenError("Token expirado") from exc
    except jwt.exceptions.InvalidTokenError as exc:
        raise ForbiddenError("Token invalido") from exc
    except jwt.exceptions.PyJWTError as exc:
        raise ForbiddenError("Sin autorización") from exc

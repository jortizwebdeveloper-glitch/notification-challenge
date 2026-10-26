import jwt
import uuid

from src.shared.settings import settings
from datetime import datetime, timedelta, timezone

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

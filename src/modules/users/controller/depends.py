from typing import Annotated

from fastapi import Depends

from ..schema.ports import UserRepositoryPort
from ..infra.user_repository import UserRepository

from sqlalchemy.orm import Session

from src.core.db import get_session

SessionDep = Annotated[Session, Depends(get_session)]


def get_user_repository(session: SessionDep):
    return UserRepository(session)


UserRepoDep = Annotated[UserRepositoryPort, Depends(get_user_repository)]

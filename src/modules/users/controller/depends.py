from typing import Annotated

from fastapi import Depends

from src.shared.depends import SessionDep

from ..infra.user_repository import UserRepository, UserRepositoryPort


def get_user_repository(session: SessionDep):
    return UserRepository(session)


UserRepoDep = Annotated[UserRepositoryPort, Depends(get_user_repository)]

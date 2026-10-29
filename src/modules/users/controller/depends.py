from typing import Annotated

from fastapi import Depends

from ..infra.user_repository import UserRepository, UserRepositoryPort

from src.shared.depends import SessionDep


def get_user_repository(session: SessionDep):
    return UserRepository(session)


UserRepoDep = Annotated[UserRepositoryPort, Depends(get_user_repository)]

from typing import Annotated

from fastapi import Depends

from src.modules.users import UserRepoDep
from src.shared.depends import SessionDep

from ..infra.repository import AuthRepository, AuthRepositoryPort
from ..infra.uow import AuthUOW
from ..service.service import AuthService


def get_auth_repository(session: SessionDep):
    return AuthRepository(session)


def get_auth_uow(s: SessionDep, a: AuthRepoDep, u: UserRepoDep):
    return AuthUOW(session=s, auth_repo=a, user_repo=u)


def get_auth_service(a: AuthRepoDep, uow: AuthUowDep):
    return AuthService(auth_repo=a, auth_uow=uow)


AuthRepoDep = Annotated[AuthRepositoryPort, Depends(get_auth_repository)]
AuthUowDep = Annotated[AuthUOW, Depends(get_auth_uow)]
AuthServiceDep = Annotated[AuthService, Depends(get_auth_service)]

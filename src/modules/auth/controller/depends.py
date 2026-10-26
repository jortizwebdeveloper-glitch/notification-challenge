from typing import Annotated

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer

from sqlalchemy.orm import Session
from src.core.db import get_session

from ..schema.ports import AuthRepositoryPort
from ..infra.auth_repository import AuthRepository
from ..infra.auth_uow import AuthUOW
from ..service.auth_service import AuthService

from src.modules.users.controller.depends import UserRepoDep

from src.shared.jwt import verify_token_jwt, jwt_error_handle


SessionDep = Annotated[Session, Depends(get_session)]


def get_auth_repository(session: SessionDep):
    return AuthRepository(session)


AuthRepoDep = Annotated[AuthRepositoryPort, Depends(get_auth_repository)]


def get_auth_uow(s: SessionDep, a: AuthRepoDep, u: UserRepoDep):
    return AuthUOW(session=s, auth_repo=a, user_repo=u)


AuthUowDep = Annotated[AuthUOW, Depends(get_auth_uow)]


def get_auth_service(a: AuthRepoDep, uow: AuthUowDep):
    return AuthService(auth_repo=a, auth_uow=uow)


AuthServiceDep = Annotated[AuthService, Depends(get_auth_service)]


oauth2_schema = OAuth2PasswordBearer(tokenUrl="signin")


def get_current_user(token: Annotated[str, Depends(oauth2_schema)]):
    with jwt_error_handle():
        payload = verify_token_jwt(token)
        return payload


AuthCurrentUserDep = Annotated[dict, Depends(get_current_user)]

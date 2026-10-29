from pwdlib import PasswordHash
from typing import Annotated

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer

from .jwt import jwt_error_handle, verify_token_jwt, TokenPayload

password_hash = PasswordHash.recommended()


def create_hash(password: str) -> str:
    return password_hash.hash(password)


def verify_hash(password: str, hash: str) -> bool:
    return password_hash.verify(password, hash)


oauth2_schema = OAuth2PasswordBearer(tokenUrl="signin")


def get_current_user(token: Annotated[str, Depends(oauth2_schema)]):
    with jwt_error_handle():
        payload = verify_token_jwt(token)
        return payload


CurrentUserDep = Annotated[TokenPayload, Depends(get_current_user)]

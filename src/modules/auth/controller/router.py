from typing import Annotated

from fastapi import APIRouter, Form

from src.shared.errors.response import get_error_response

from ..schema.dto import SigninRequest, SignupRequest
from .depends import AuthServiceDep

auth = APIRouter(prefix="", tags=["Auth"])


@auth.post("/signup", status_code=201, responses=get_error_response(409), summary="Registrar usuario")
def auth_signup(
    form_data: Annotated[SignupRequest, Form()],
    service: AuthServiceDep,
):
    return service.signup_user(email=form_data.email, password=form_data.password)


@auth.post("/signin", responses=get_error_response(), summary="Iniciar sesión")
def auth_signin(
    form_data: Annotated[SigninRequest, Form()],
    service: AuthServiceDep,
):
    return service.signin_user(form_data.username, form_data.password)

from typing import Annotated

from fastapi import APIRouter, Form

from .depends import AuthServiceDep, AuthCurrentUserDep
from ..schema.dto import SigninRequest, SignupRequest

auth = APIRouter(prefix="")


@auth.post("/signin")
def auth_signin(
    form_data: Annotated[SigninRequest, Form()],
    service: AuthServiceDep,
):
    return service.signin_user(form_data.email, form_data.password)


@auth.post("/signup")
def auth_signup(
    form_data: Annotated[SignupRequest, Form()],
    service: AuthServiceDep,
):
    return service.signup_user(email=form_data.email, password=form_data.password)


@auth.post("/signon")
def auth_signon(payload: AuthCurrentUserDep):
    return payload

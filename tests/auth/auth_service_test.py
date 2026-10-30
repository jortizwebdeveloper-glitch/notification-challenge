from unittest.mock import ANY, MagicMock

import pytest

from src.modules.auth.infra.auth_repository import AuthRepository
from src.modules.auth.infra.auth_uow import AuthUOW
from src.modules.auth.service.auth_service import AuthService
from src.shared.auth import create_hash
from src.shared.errors.exceptions import AuthenticationError
from src.shared.jwt import verify_token_jwt

EMAIL = "test@test.com"
PASSWORD = "1234"


@pytest.fixture
def auth_repo():
    return MagicMock(spec=AuthRepository)


@pytest.fixture
def auth_uow():
    return MagicMock(spec=AuthUOW)


@pytest.fixture
def auth_service(auth_repo, auth_uow):
    return AuthService(auth_repo, auth_uow)


@pytest.fixture
def user():
    return MagicMock(user_id=1, password=create_hash(PASSWORD))


def test_auth_service_signin_user_successful(auth_service, auth_repo, user):
    auth_repo.find_by_email.side_effect = lambda email: user if EMAIL == email else None

    result = auth_service.signin_user(EMAIL, PASSWORD)
    payload = verify_token_jwt(result["access_token"])
    assert payload["sub"] == "1"


def test_auth_service_signin_user_error_user_not_found(auth_service, auth_repo):
    auth_repo.find_by_email.return_value = None

    with pytest.raises(AuthenticationError):
        auth_service.signin_user(EMAIL, PASSWORD)


def test_auth_service_signin_user_error_password_incorrect(
    auth_service, auth_repo, user
):
    auth_repo.find_by_email.return_value = user

    with pytest.raises(AuthenticationError):
        auth_service.signin_user(EMAIL, "4321")


def test_auth_service_signup_user(auth_service, auth_uow):
    result = auth_service.signup_user(EMAIL, PASSWORD)

    auth_uow.register_auth_user.assert_called_once_with(EMAIL, ANY)
    _, stored_password = auth_uow.register_auth_user.call_args.args
    assert stored_password != PASSWORD
    assert result == {"msg": "Registro realizado exitosamente"}

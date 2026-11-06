from unittest.mock import ANY, MagicMock

import pytest

from src.modules.auth import AuthRepository, AuthService, AuthUOW
from src.modules.user import UserRepository
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
def user_repo():
    return MagicMock(spec=UserRepository)


@pytest.fixture
def auth_service(auth_repo, auth_uow, user_repo):
    return AuthService(auth_repo, auth_uow, user_repo)


@pytest.fixture
def user():
    return MagicMock(id=1, email=EMAIL)


@pytest.fixture
def auth():
    return MagicMock(user_id=1, password=create_hash(PASSWORD))


def test_auth_service_signin_user_successful(
    auth_service, auth_repo, user_repo, auth, user
):
    user_repo.find_by_email.side_effect = lambda email: (
        user if user.email == email else None
    )
    auth_repo.find_by_user_id.side_effect = lambda id: (
        auth if auth.user_id == id else None
    )

    result = auth_service.signin_user(EMAIL, PASSWORD)
    payload = verify_token_jwt(result["access_token"])
    assert payload["sub"] == "1"


def test_auth_service_signin_user_error_user_not_found(auth_service, auth_repo):
    auth_repo.find_by_user_id.return_value = None

    with pytest.raises(AuthenticationError):
        auth_service.signin_user(EMAIL, PASSWORD)


def test_auth_service_signin_user_error_password_incorrect(
    auth_service, auth_repo, auth
):
    auth_repo.find_by_user_id.return_value = auth

    with pytest.raises(AuthenticationError):
        auth_service.signin_user(EMAIL, "4321")


def test_auth_service_signup_user(auth_service, auth_uow):
    result = auth_service.signup_user(EMAIL, PASSWORD)

    auth_uow.register_auth_user.assert_called_once_with(EMAIL, ANY)
    _, stored_password = auth_uow.register_auth_user.call_args.args
    assert stored_password != PASSWORD
    assert result == {"msg": "Registro realizado exitosamente"}

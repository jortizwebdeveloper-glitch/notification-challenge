from unittest.mock import MagicMock

import pytest
from sqlalchemy.orm import Session

from src.modules.auth.infra.auth_repository import AuthRepository
from src.modules.auth.infra.auth_uow import AuthUOW
from src.modules.users.infra.user_repository import UserRepository

EMAIL = "test@email.com"
PASSWORD = "hash"


@pytest.fixture
def session():
    return MagicMock(spec=Session)


@pytest.fixture
def user_repository():
    return MagicMock(spec=UserRepository)


@pytest.fixture
def auth_repository():
    return MagicMock(spec=AuthRepository)


@pytest.fixture
def auth_uow(session, auth_repository, user_repository):
    return AuthUOW(
        session=session, user_repo=user_repository, auth_repo=auth_repository
    )


def test_auth_uow_register_auth_user(auth_uow):
    result = auth_uow.register_auth_user(EMAIL, PASSWORD)

    assert result is True

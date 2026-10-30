import pytest

from src.modules.users.infra.user_model import UserModel
from src.modules.users.infra.user_repository import UserRepository
from src.shared.errors.exceptions import AlreadyExistsError
from tests.helpers import addUser

EMAIL = "test@email.com"


@pytest.fixture
def user_repository(session):
    return UserRepository(session)


def test_user_repository_create(user_repository):
    user = user_repository.create(EMAIL)

    assert type(user) == UserModel


def test_user_repository_email_unique_error(session, user_repository):
    addUser(session, EMAIL)
    session.expunge_all()

    with pytest.raises(AlreadyExistsError):
        user_repository.create(EMAIL)

import pytest

from src.modules.auth.infra.auth_model import AuthModel
from src.modules.users.infra.user_model import UserModel

from src.modules.auth.infra.auth_repository import AuthRepository

from tests.helpers import addUser, addAuth


EMAIL = "test@email.com"
PASSWORD = "hash"


@pytest.fixture
def auth_repository(session):
    return AuthRepository(session)


def test_auth_repository_find_by_email_success(session, auth_repository):
    # Arrange: se siembra directo con los modelos, sin pasar por otros repos
    user = addUser(session, email=EMAIL)
    addAuth(session, password=PASSWORD, user_id=user.id)
    session.expunge_all()  # fuerza a que la consulta cargue desde la BD

    # Act
    result = auth_repository.find_by_email(EMAIL)
    # Assert
    assert result is not None
    assert result.password == PASSWORD
    assert result.user.email == EMAIL


def test_auth_repository_create_success(session, auth_repository):
    user = addUser(session, email=EMAIL)
    session.expunge_all()

    result = auth_repository.create(PASSWORD, user.id)

    assert result is not None
    assert result.password == PASSWORD
    assert result.user_id == user.id

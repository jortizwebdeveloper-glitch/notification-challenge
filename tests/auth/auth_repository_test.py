import pytest
import pprint

from src.modules.auth.infra.auth_model import AuthModel
from src.modules.auth.infra.auth_repository import AuthRepository
from src.modules.users.infra.user_model import UserModel


@pytest.fixture
def auth_repository(session):
    return AuthRepository(session)


def test_find_by_email_existente_devuelve_auth_con_usuario(session, auth_repository):
    # Arrange: se siembra directo con los modelos, sin pasar por otros repos
    user = UserModel(email="test@test.com")
    session.add(user)
    session.flush()
    session.add(AuthModel(password="hash", user_id=user.id))
    session.flush()
    session.expunge_all()  # fuerza a que la consulta cargue desde la BD

    # Act
    result = auth_repository.find_by_email("test@test.com")
    # Assert
    assert result is not None
    assert result.password == "hash"
    assert result.user.email == "test@test.com"

from src.shared.auth import create_hash, verify_hash
from src.shared.errors import AuthenticationError
from src.shared.jwt import create_token_jwt

from ..infra.uow import AuthUOW
from ..schema.ports import AuthRepositoryPort
from src.modules.user import UserRepositoryPort


class AuthService:
    def __init__(
        self,
        auth_repo: AuthRepositoryPort,
        auth_uow: AuthUOW,
        user_repo: UserRepositoryPort,
    ):
        self._auth_repo = auth_repo
        self._user_repo = user_repo
        self._auth_uow = auth_uow

    def signin_user(self, email: str, password: str):
        user = self._user_repo.find_by_email(email)

        if not user:
            raise AuthenticationError("Usuario no registrado")

        auth = self._auth_repo.find_by_user_id(user.id)

        if auth and verify_hash(password, auth.password):
            return {"access_token": create_token_jwt(str(auth.user_id))}

        raise AuthenticationError("Accesos invalidos")

    def signup_user(self, email: str, password: str):
        self._auth_uow.register_auth_user(email, create_hash(password))

        return {"msg": "Registro realizado exitosamente"}

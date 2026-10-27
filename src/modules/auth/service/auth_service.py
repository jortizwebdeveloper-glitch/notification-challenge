from ..schema.ports import AuthRepositoryPort
from ..infra.auth_uow import AuthUOW
from src.shared.auth import create_hash, verify_hash
from src.shared.jwt import create_token_jwt
from src.shared.errors import AuthenticationError


class AuthService:
    def __init__(self, auth_repo: AuthRepositoryPort, auth_uow: AuthUOW):
        self._auth_repo = auth_repo
        self._auth_uow = auth_uow

    def signin_user(self, email: str, password: str):
        auth = self._auth_repo.find_by_email(email)

        if auth and verify_hash(password, auth.password):
            return {"token": create_token_jwt(str(auth.user_id))}

        raise AuthenticationError("Accesos invalidos")

    def signup_user(self, email: str, password: str):
        self._auth_uow.register_auth_user(email, create_hash(password))

        return {"msg": "Registro relaizado exitosamente"}

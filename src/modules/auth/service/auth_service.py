from ..schema.ports import AuthRepositoryPort
from ..infra.auth_uow import AuthUOW
from src.shared.auth import create_hash, verify_hash
from src.shared.jwt import create_token_jwt, jwt_error_handle


class AuthService:
    def __init__(self, auth_repo: AuthRepositoryPort, auth_uow: AuthUOW):
        self._auth_repo = auth_repo
        self._auth_uow = auth_uow

    def signin_user(self, email: str, password: str):
        auth = self._auth_repo.find_by_email(email)

        if auth and verify_hash(password, auth.password):
            return {"token": create_token_jwt(str(auth.user_id))}

        return {"msg": "Accesos incorrectos"}

    def signup_user(self, email: str, password: str):
        result = self._auth_uow.register_auth_user(email, create_hash(password))

        return {"msg": "Registro relaizado exitosamente"}

from sqlalchemy.orm import Session

from src.core.db.exceptions import transaction_db
from src.modules.user import UserRepositoryPort

from ..schema.ports import AuthRepositoryPort


class AuthUOW:
    def __init__(
        self,
        auth_repo: AuthRepositoryPort,
        user_repo: UserRepositoryPort,
        session: Session,
    ):
        self._session = session

        self._auth_repo = auth_repo
        self._user_repo = user_repo

    def register_auth_user(self, email: str, password: str):
        with transaction_db(self._session):
            user = self._user_repo.create(email)

            self._auth_repo.create(password, user.id)
            self._session.commit()
            return True

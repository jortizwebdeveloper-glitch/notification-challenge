from sqlalchemy.orm import Session

from ..schema.exceptions import user_db_errors
from ..schema.ports import UserRepositoryPort
from .user_model import UserModel


class UserRepository(UserRepositoryPort):
    def __init__(self, session: Session):
        self._session = session

    def create(self, email):
        user = UserModel(email=email)
        with user_db_errors():
            self._session.add(user)
            self._session.flush()
            return user

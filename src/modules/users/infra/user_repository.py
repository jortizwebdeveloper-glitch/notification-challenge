from sqlalchemy.orm import Session
from sqlalchemy import select

from .user_model import UserModel
from ..schema.ports import UserRepositoryPort
from ..schema.exceptions import user_db_errors


class UserRepository(UserRepositoryPort):
    def __init__(self, session: Session):
        self._session = session

    def create(self, email):
        user = UserModel(email=email)
        with user_db_errors():
            self._session.add(user)
            self._session.flush()
            return user

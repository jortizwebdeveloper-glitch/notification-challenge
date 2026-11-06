from sqlalchemy import select
from sqlalchemy.orm import Session

from ..schema.exceptions import user_db_errors
from ..schema.ports import UserRepositoryPort
from .model import UserModel


class UserRepository(UserRepositoryPort):
    def __init__(self, session: Session):
        self._session = session

    def find_by_email(self, email: str) -> UserModel | None:
        stmt = select(UserModel).where(UserModel.email == email)
        user = self._session.scalar(stmt)
        return user

    def create(self, email) -> UserModel:
        user = UserModel(email=email)
        with user_db_errors():
            self._session.add(user)
            self._session.flush()
            return user

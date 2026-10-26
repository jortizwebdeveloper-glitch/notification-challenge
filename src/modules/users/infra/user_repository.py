from sqlalchemy.orm import Session
from sqlalchemy import select

from .user_model import UserModel
from ..schema.ports import UserRepositoryPort


class UserRepository(UserRepositoryPort):
    def __init__(self, session: Session):
        self._session = session

    def find_by_email(self, email: str):
        user = self._session.scalars(
            select(UserModel).where(UserModel.email == email)
        ).one_or_none()
        return user

    def create(self, email):
        user = UserModel(email=email)
        self._session.add(user)
        self._session.flush()
        return user

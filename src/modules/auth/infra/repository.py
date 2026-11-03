from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload, load_only

from src.modules.users import UserModel

from ..schema.ports import AuthRepositoryPort
from .model import AuthModel


class AuthRepository(AuthRepositoryPort):
    def __init__(self, session: Session):
        self._session = session

    def find_by_email(self, email: str) -> AuthModel | None:
        stmt = (
            select(AuthModel)
            .options(
                load_only(AuthModel.password),
                joinedload(AuthModel.user).load_only(UserModel.email),
            )
            .join(AuthModel.user)
            .where(UserModel.email == email)
        )

        row = self._session.scalars(stmt).one_or_none()

        return row

    def create(self, password, user_id):
        auth = AuthModel(password=password, user_id=user_id)
        self._session.add(auth)
        self._session.flush()
        return auth

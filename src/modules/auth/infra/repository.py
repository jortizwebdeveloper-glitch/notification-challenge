from sqlalchemy import select
from sqlalchemy.orm import Session, load_only

from ..schema.ports import AuthRepositoryPort
from .model import AuthModel


class AuthRepository(AuthRepositoryPort):
    def __init__(self, session: Session):
        self._session = session

    def find_by_user_id(self, user_id: int) -> AuthModel | None:
        stmt = (
            select(AuthModel)
            .options(
                load_only(AuthModel.password),
            )
            .where(AuthModel.user_id == user_id)
        )

        row = self._session.scalars(stmt).one_or_none()

        return row

    def create(self, password, user_id) -> AuthModel:
        auth = AuthModel(password=password, user_id=user_id)
        self._session.add(auth)
        self._session.flush()
        return auth

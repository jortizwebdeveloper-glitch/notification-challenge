from sqlalchemy import delete, insert, select, update
from sqlalchemy.orm import Session, defer

from ..schema.dto import NotificationData
from ..schema.ports import NotificationRepositoryPort
from .model import NotificationModel


class NotificationRepository(NotificationRepositoryPort):
    def __init__(self, session: Session):
        self._session = session

    def find_by_id(self, id):
        return self._session.get(NotificationModel, id)

    def find_all_by_user_id(self, user_id: int):
        stmt = (
            select(NotificationModel)
            .options(defer(NotificationModel.user_id))
            .where(NotificationModel.user_id == user_id)
        )
        rows = self._session.scalars(stmt).all()
        return rows

    def find_by_user_id(self, id: int, user_id: int):
        stmt = (
            select(NotificationModel)
            .options(defer(NotificationModel.user_id))
            .where(NotificationModel.user_id == user_id, NotificationModel.id == id)
        )
        row = self._session.scalars(stmt).one_or_none()
        return row

    def create(self, body: NotificationData, user_id):
        stmt = (
            insert(NotificationModel)
            .values(**body, user_id=user_id)
            .options(defer(NotificationModel.user_id))
            .returning(NotificationModel)
        )
        row = self._session.scalars(stmt).one()
        self._session.commit()
        self._session.refresh(row)
        return row

    def update(self, body: NotificationData, id: int, user_id: int):
        stmt = (
            update(NotificationModel)
            .values(**body)
            .options(defer(NotificationModel.user_id))
            .where(NotificationModel.id == id, NotificationModel.user_id == user_id)
            .returning(NotificationModel)
        )
        row = self._session.scalars(stmt).one_or_none()
        self._session.commit()
        self._session.refresh(row)

        return row

    def delete(self, id, user_id) -> int:
        stmt = delete(NotificationModel).where(
            NotificationModel.id == id, NotificationModel.user_id == user_id
        )
        result = self._session.execute(stmt)
        self._session.commit()
        return result.rowcount

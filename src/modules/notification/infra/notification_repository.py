from sqlalchemy import select
from sqlalchemy.orm import Session, defer

from ..schema.ports import NotificationRepositoryPort
from .notification_model import NotificationModel


class NotificationRepository(NotificationRepositoryPort):
    def __init__(self, session: Session):
        self._session = session

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
        rows = self._session.scalars(stmt).one_or_none()
        return rows

    def create(self, user_id):
        return super().create(user_id)

    def update(self, id, user_id):
        return super().update(id, user_id)

    def delete(self, id, user_id):
        return super().delete(id, user_id)

from ..schema.ports import NotificationRepositoryPort

from sqlalchemy.orm import Session, defer
from sqlalchemy import select

from .notification_model import NotificationModel


class NotificationRepository(NotificationRepositoryPort):
    def __init__(self, session: Session):
        self._session = session

    def find_by_user_id(self, user_id: int):
        rows = self._session.scalars(
            select(NotificationModel)
            .options(defer(NotificationModel.user_id))
            .where(NotificationModel.user_id == user_id)
        ).all()
        return rows

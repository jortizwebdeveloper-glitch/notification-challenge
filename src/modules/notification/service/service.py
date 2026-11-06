from src.shared.errors.exceptions import NotFoundError

from ..schema.dto import NotificationData
from ..schema.ports import NotificationRepositoryPort


class NotificationService:
    def __init__(self, noti_repo: NotificationRepositoryPort):
        self._noti_repo = noti_repo

    def get_all_notifications_by_user(self, user_id: int):
        return self._noti_repo.find_all_by_user_id(user_id)

    def get_notification_by_user(self, id: int, user_id: int):
        row = self._noti_repo.find_by_user_id(id, user_id)
        if not row:
            raise NotFoundError("Notificacion inexistente")
        return row

    def create_notification_by_user(self, body: NotificationData, user_id: int):
        return self._noti_repo.create(body, user_id)

    def update_notification_by_user(
        self, body: NotificationData, id: int, user_id: int
    ):
        row = self._noti_repo.update(body, id, user_id)
        if not row:
            raise NotFoundError("Notificacion inexistente")
        return row

    def delete_notification_by_user(self, id: int, user_id: int):
        row = self._noti_repo.delete(id, user_id)
        if row == 0:
            raise NotFoundError("Notificacion inexistente")

        return row

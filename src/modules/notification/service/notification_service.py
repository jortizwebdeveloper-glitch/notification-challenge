from ..schema.ports import NotificationRepositoryPort


class NotificationService:
    def __init__(self, notitfication_repository: NotificationRepositoryPort):
        self._noti_repo = notitfication_repository

    def get_all_notifications_by_user(self, user_id: int):
        return self._noti_repo.find_all_by_user_id(user_id)

    def get_notification_by_user(self, id: int, user_id: int):
        return self._noti_repo.find_by_user_id(id, user_id)

from src.shared.channels import ChannelData, get_channel

from ..schema.dto import NotificationData
from ..schema.ports import NotificationRepositoryPort


class NotificationService:
    def __init__(self, notitfication_repository: NotificationRepositoryPort):
        self._noti_repo = notitfication_repository

    def send(self, id: int):
        row = self._noti_repo.find_by_id(id)

        if row is not None:
            channel = get_channel(
                ChannelData(
                    title=row.title,
                    content=row.content,
                    channel=row.channel,
                    to="test@test.com",
                )
            )
            if channel:
                print(channel.send())
            else:
                print("Invalid channel:", row.channel)

        return row

    def get_all_notifications_by_user(self, user_id: int):
        return self._noti_repo.find_all_by_user_id(user_id)

    def get_notification_by_user(self, id: int, user_id: int):
        return self._noti_repo.find_by_user_id(id, user_id)

    def create_notification_by_user(self, body: NotificationData, user_id: int):
        return self._noti_repo.create(body, user_id)

    def update_notification_by_user(
        self, body: NotificationData, id: int, user_id: int
    ):
        return self._noti_repo.update(body, id, user_id)

    def delete_notification_by_user(self, id: int, user_id: int):
        return self._noti_repo.delete(id, user_id)

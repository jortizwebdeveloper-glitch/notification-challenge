import asyncio

from arq import ArqRedis

from src.shared.channels import ChannelData, get_channel
from src.shared.errors.exceptions import NotFoundError

from ..schema.dto import NotificationData
from ..schema.ports import NotificationRepositoryPort


class NotificationService:
    def __init__(
        self, notitfication_repository: NotificationRepositoryPort, arq: ArqRedis
    ):
        self._noti_repo = notitfication_repository
        self._arq = arq

    async def send(self, id: int, user_id: int):
        row = self._noti_repo.find_by_user_id(id, user_id)

        if row is not None:
            data = ChannelData(
                title=row.title, content=row.content, channel=row.channel
            )
            channel = get_channel(data)
            job_ids = []
            emails = await asyncio.to_thread(channel.open_src)
            for email in emails:
                data.to = email
                job = await self._arq.enqueue_job("send_notification", data)
                job_ids.append(job.job_id)

            return {"job_ids": job_ids}
        else:
            raise NotFoundError("Notificación no encontrada")

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

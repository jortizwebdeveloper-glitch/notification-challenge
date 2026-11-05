import asyncio

from arq import ArqRedis

from src.modules.notification import NotificationRepositoryPort
from src.shared.channels import ChannelData, get_channel
from src.shared.errors.exceptions import NotFoundError

from ..schema.ports import SendRepositoryPort


class SendService:
    def __init__(
        self,
        noti_repo: NotificationRepositoryPort,
        send_repo: SendRepositoryPort,
        arq: ArqRedis,
    ):
        self._noti_repo = noti_repo
        self._send_repo = send_repo
        self._arq = arq

    def get_all_send_notifications(self, user_id: int):
        return self._send_repo.find_all_by_user_id(user_id)

    async def send_notification_by_id(self, id: int, user_id: int):
        row = self._noti_repo.find_by_user_id(id, user_id)

        if row is not None:
            data = ChannelData(
                title=row.title, content=row.content, channel=row.channel
            )
            channel = get_channel(data)
            job_ids = []
            src = await asyncio.to_thread(channel.open_src)
            for to in src:
                data.to = to
                job = await self._arq.enqueue_job(
                    "send_notification", {"data": data, "user_id": user_id}
                )
                job_ids.append(job.job_id)

            return {"job_ids": job_ids}
        else:
            raise NotFoundError("Notificación no encontrada")

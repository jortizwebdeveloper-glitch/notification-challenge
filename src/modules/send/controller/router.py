from fastapi import APIRouter

from src.shared.auth import CurrentUserDep

from .depends import SendServiceDep

send = APIRouter(prefix="/send")


@send.get("")
def get_send_notifications(payload: CurrentUserDep, send_service: SendServiceDep):
    return send_service.get_all_send_notifications(int(payload["sub"]))


@send.post("/{id}")
async def send_notifications(
    payload: CurrentUserDep, send_service: SendServiceDep, id: int
):
    return await send_service.send_notification_by_id(id, int(payload["sub"]))

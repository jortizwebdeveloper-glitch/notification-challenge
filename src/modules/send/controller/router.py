from typing import Annotated

from fastapi import APIRouter, Path

from src.shared.auth import CurrentUserDep
from src.shared.errors.response import get_error_response

from .depends import SendServiceDep

send = APIRouter(prefix="/send", tags=["Send"])


@send.get("", summary="Registro de envios")
def get_send_notifications(payload: CurrentUserDep, send_service: SendServiceDep):
    return send_service.get_all_send_notifications(int(payload["sub"]))


@send.post("/{id}", responses=get_error_response(), summary="Envio de notificación")
async def send_notifications(
    payload: CurrentUserDep,
    send_service: SendServiceDep,
    id: Annotated[int, Path(description="ID de la notificación a enviar")],
):
    return await send_service.send_notification_by_id(id, int(payload["sub"]))

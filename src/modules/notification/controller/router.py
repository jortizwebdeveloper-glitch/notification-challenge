import asyncio
from typing import Annotated

from fastapi import APIRouter, Query

from src.modules.send import SendServiceDep
from src.shared.auth import CurrentUserDep
from src.shared.errors.response import get_error_response

from ..schema.dto import (
    CreateNotificationRequest,
    NotificationData,
    ResponseCreateNotification,
    ResponseNotification,
    UpdateNotificationRequest,
)
from .depends import NotiServiceDep

notification = APIRouter(
    prefix="/notifications",
    tags=["Notifications"],
)


@notification.get(
    "",
    response_model=list[ResponseNotification],
    summary="Lista de notificaciones"
)
def get_notifications(payload: CurrentUserDep, noti_service: NotiServiceDep):
    return noti_service.get_all_notifications_by_user(int(payload["sub"]))


@notification.post(
    "", response_model=ResponseCreateNotification, responses=get_error_response(),
    summary="Crear notificación"
)
async def create_notification(
    payload: CurrentUserDep,
    body: CreateNotificationRequest,
    noti_service: NotiServiceDep,
    send_service: SendServiceDep,
    send: Annotated[
        bool,
        Query(
            description="Define si se genera el envio por el canal definido al momento de crear la notificacion"
        ),
    ] = False,
):
    data = NotificationData(**body.model_dump())
    user_id = int(payload["sub"])
    noti = await asyncio.to_thread(
        lambda: noti_service.create_notification_by_user(data, user_id)
    )

    response = {"notification": noti}

    if send:
        jobs_ids = await send_service.send_notification_by_id(noti.id, user_id)
        response["jobs_ids"] = jobs_ids["job_ids"]

    return response


item = APIRouter(prefix="/{id}")


@item.get(
    "",
    response_model=ResponseNotification | None,
    summary="Obtener notificación",
    responses=get_error_response(404),
)
def get_notification(payload: CurrentUserDep, noti_service: NotiServiceDep, id: int):
    return noti_service.get_notification_by_user(id, int(payload["sub"]))


@item.put(
    "",
    response_model=ResponseNotification,
    summary="Actualizar notificación",
    responses=get_error_response(404),
)
def update_notification(
    payload: CurrentUserDep,
    body: UpdateNotificationRequest,
    noti_service: NotiServiceDep,
    id: int,
):
    data = NotificationData(**body.model_dump(exclude_none=True))
    return noti_service.update_notification_by_user(data, id, int(payload["sub"]))


@item.delete(
    "",
    response_model=int,
    summary="Eliminar notificación",
    responses=get_error_response(404),
)
def delete_notification(
    payload: CurrentUserDep,
    noti_service: NotiServiceDep,
    id: int,
):
    return noti_service.delete_notification_by_user(id, int(payload["sub"]))


notification.include_router(item)

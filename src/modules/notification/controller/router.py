import asyncio

from fastapi import APIRouter

from src.modules.send import SendServiceDep
from src.shared.auth import CurrentUserDep

from ..schema.dto import (
    CreateNotificationRequest,
    NotificationData,
    UpdateNotificationRequest,
)
from .depends import NotiServiceDep

notification = APIRouter(
    prefix="/notifications",
    tags=["Notifications"],
)


@notification.get("")
def get_notifications(payload: CurrentUserDep, noti_service: NotiServiceDep):
    return noti_service.get_all_notifications_by_user(int(payload["sub"]))


@notification.post("")
async def create_notification(
    payload: CurrentUserDep,
    body: CreateNotificationRequest,
    noti_service: NotiServiceDep,
    send_service: SendServiceDep,
    send: bool = False,
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


@item.get("")
def get_notification(payload: CurrentUserDep, noti_service: NotiServiceDep, id: int):
    return noti_service.get_notification_by_user(id, int(payload["sub"]))


@item.put("")
def update_notification(
    payload: CurrentUserDep,
    body: UpdateNotificationRequest,
    noti_service: NotiServiceDep,
    id: int,
):
    data = NotificationData(**body.model_dump(exclude_none=True))
    return noti_service.update_notification_by_user(data, id, int(payload["sub"]))


@item.delete("")
def delete_notification(
    payload: CurrentUserDep,
    noti_service: NotiServiceDep,
    id: int,
):
    return noti_service.delete_notification_by_user(id, int(payload["sub"]))


notification.include_router(item)

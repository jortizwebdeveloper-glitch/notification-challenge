from fastapi import APIRouter

from src.shared.errors.response import COMMON_REPONSES

from ..schema.dto import CreateNotificationRequest
from .depends import CurrentUserDep, NotiServiceDep

notification = APIRouter(
    prefix="/notifications",
    tags=["Notifications"],
    #   dependencies=[current_user_depends]
)


@notification.get("")
def get_notifications(payload: CurrentUserDep, noti_service: NotiServiceDep):
    return noti_service.get_all_notifications_by_user(int(payload["sub"]))


@notification.post("", responses=COMMON_REPONSES)
def create_notification(body: CreateNotificationRequest):
    return body


item = APIRouter(prefix="/{id}")


@item.get("")
def get_notification(payload: CurrentUserDep, noti_service: NotiServiceDep, id: int):
    return noti_service.get_notification_by_user(id, int(payload["sub"]))


notification.include_router(item)

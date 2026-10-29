from fastapi import APIRouter

from .depends import CurrentUserDep, NotiServiceDep, current_user_depends

notification = APIRouter(
    prefix="/notifications", tags=["Notifications"], dependencies=[current_user_depends]
)


@notification.get("")
def get_notification(payload: CurrentUserDep, noti_service: NotiServiceDep):
    return noti_service.get_notifications_by_user(int(payload["sub"]))

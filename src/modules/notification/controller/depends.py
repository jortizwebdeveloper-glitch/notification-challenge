from typing import Annotated, get_args

from ..infra.notification_repository import (
    NotificationRepository,
    NotificationRepositoryPort,
)
from ..service.notification_service import NotificationService


from fastapi import Depends

from src.shared.depends import SessionDep
from src.shared.auth import CurrentUserDep

_, current_user_depends = get_args(CurrentUserDep)


def get_noti_repository(session: SessionDep):
    return NotificationRepository(session)


def get_noti_service(repository: NotiRepositoryDep):
    return NotificationService(notitfication_repository=repository)


NotiRepositoryDep = Annotated[NotificationRepositoryPort, Depends(get_noti_repository)]
NotiServiceDep = Annotated[NotificationService, Depends(get_noti_service)]

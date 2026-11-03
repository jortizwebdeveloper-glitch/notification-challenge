from typing import Annotated, get_args

from fastapi import Depends

from src.core.arq import ArqDep
from src.shared.auth import CurrentUserDep
from src.shared.depends import SessionDep

from ..infra.repository import (
    NotificationRepository,
    NotificationRepositoryPort,
)
from ..service.service import NotificationService

_, current_user_depends = get_args(CurrentUserDep)


def get_noti_repository(session: SessionDep):
    return NotificationRepository(session)


def get_noti_service(repository: NotiRepositoryDep, arq: ArqDep):
    return NotificationService(notitfication_repository=repository, arq=arq)


NotiRepositoryDep = Annotated[NotificationRepositoryPort, Depends(get_noti_repository)]
NotiServiceDep = Annotated[NotificationService, Depends(get_noti_service)]

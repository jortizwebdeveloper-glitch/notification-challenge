from typing import Annotated

from fastapi import Depends

from src.modules.notification import NotiRepositoryDep
from src.shared.depends import ArqDep, AsyncSessionDep, SessionDep

from ..infra.repository import SendRepository
from ..schema.ports import SendRepositoryPort
from ..service.service import SendService


def get_send_repository(session: SessionDep, async_session: AsyncSessionDep):
    return SendRepository(session=session, async_session=async_session)


def get_send_service(
    noti_repo: NotiRepositoryDep, send_repo: SendRepositoryDep, arq: ArqDep
):
    return SendService(noti_repo=noti_repo, send_repo=send_repo, arq=arq)


SendRepositoryDep = Annotated[SendRepositoryPort, Depends(get_send_repository)]
SendServiceDep = Annotated[SendService, Depends(get_send_service)]

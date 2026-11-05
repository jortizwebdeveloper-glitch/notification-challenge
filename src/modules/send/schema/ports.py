from abc import ABC, abstractmethod

from ..infra.model import SendModel
from .dto import SendData


class SendRepositoryPort(ABC):
    @abstractmethod
    def find_all_by_user_id(self, user_id: int) -> list[SendModel]:
        pass

    @abstractmethod
    async def async_create(self, body: SendData, user_id: int) -> SendModel:
        pass

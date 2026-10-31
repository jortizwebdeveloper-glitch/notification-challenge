from abc import ABC, abstractmethod

from ..infra.model import NotificationModel


class NotificationRepositoryPort(ABC):
    @abstractmethod
    def find_all_by_user_id(self, user_id: int) -> list[NotificationModel]:
        pass

    @abstractmethod
    def find_by_user_id(self, id: int, user_id: int) -> NotificationModel | None:
        pass

    @abstractmethod
    def create(self, user_id: int) -> NotificationModel:
        pass

    @abstractmethod
    def update(self, id: int, user_id: int) -> int:
        pass

    @abstractmethod
    def delete(self, id: int, user_id: int) -> int:
        pass

from abc import ABC, abstractmethod


class NotificationRepositoryPort(ABC):
    @abstractmethod
    def find_by_user_id(self, user_id: int):
        pass

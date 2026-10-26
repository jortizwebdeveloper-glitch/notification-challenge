from abc import ABC, abstractmethod


class AuthRepositoryPort(ABC):
    @abstractmethod
    def find_by_email(self, user_id: int):
        pass

    @abstractmethod
    def create(self, password: str, user_id: int):
        pass

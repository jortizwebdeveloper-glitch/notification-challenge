from abc import ABC, abstractmethod


class UserRepositoryPort(ABC):
    @abstractmethod
    def find_by_email(self, email: str):
        pass

    @abstractmethod
    def create(self, email:str):
        pass

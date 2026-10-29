from abc import ABC, abstractmethod


class UserRepositoryPort(ABC):
    @abstractmethod
    def create(self, email:str):
        pass

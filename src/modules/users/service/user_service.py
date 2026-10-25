from ..schema.ports import UserRepositoryPort


class USerService:
    def __init__(self, user_repository: UserRepositoryPort):
        self._user_repository = user_repository

    def get_user(self, email: str):
        return self._user_repository.find_by_email(email)

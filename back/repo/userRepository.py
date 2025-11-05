from abc import ABC, abstractmethod
from models.user import User
from schemas.user import UserCreate

class UserRepository(ABC):
    @abstractmethod
    async def get_user_by_id(self, id: int) -> User | None:
        pass

    @abstractmethod
    async def get_user_by_username(self, username: str) -> User | None:
        pass

    @abstractmethod
    async def create_user(self, data: UserCreate) -> User | None:
        pass

from abc import ABC, abstractmethod
from models.refresh_token import RefreshToken
from schemas.token import RefreshCreate

class RefreshTokenRepository(ABC):
    @abstractmethod
    async def get_token_by_hash(self, token_hash: str) -> RefreshToken | None:
        pass

    @abstractmethod
    async def create_token(self, data: RefreshCreate) -> RefreshToken | None:
        pass

    @abstractmethod
    async def get_token_by_user(self, user_id: int) -> list[RefreshToken]: 
        pass
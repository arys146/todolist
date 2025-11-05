from abc import ABC, abstractmethod
from models.habbit import Habbit
from schemas.habbit import HabbitCreate

class HabbitRepository(ABC):
    @abstractmethod
    async def get_habbit_by_id(self, id: int) -> Habbit | None:
        pass

    @abstractmethod
    async def create_habbit(self, data: HabbitCreate, user_id: int) -> Habbit | None:
        pass

    @abstractmethod
    async def get_habbits_by_user(self, user_id:int) -> list[Habbit]: 
        pass
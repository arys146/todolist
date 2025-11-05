from abc import ABC, abstractmethod
from models.habbit_tracker import HabbitTracker
from schemas.habbitCheck import HabbitTrackerCreate

class HabbitTrackerRepository(ABC):    
    @abstractmethod
    async def get_by_day(self, create : HabbitTrackerCreate) -> HabbitTracker | None:
        pass
    
    @abstractmethod
    async def check(self, create : HabbitTrackerCreate) -> HabbitTracker:
        pass
    
    @abstractmethod
    async def uncheck(self, create : HabbitTrackerCreate) -> int:
        pass
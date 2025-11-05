from abc import ABC, abstractmethod

class RamStorage(ABC): 
    @abstractmethod
    async def add(self, user_id: int, sid: str, ttl_sec: int) -> None:
        pass

    @abstractmethod
    async def contains(self, user_id: int, sid: str, ttl_sec: int = 0) -> bool:
        pass

    @abstractmethod
    async def remove(self, user_id: int, sid: str) -> None:
        pass

    @abstractmethod
    async def remove_all(self, user_id: int) -> None: 
        pass
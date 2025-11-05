from redis import asyncio as aioredis
from .ramStorage import RamStorage


class RedisStorage(RamStorage): 
    def __init__(self, client: aioredis.Redis):
        self.r = client 

    @staticmethod 
    def _user_key(uid: int) -> str:
        return f"auth:sessions:{uid}"
    
    async def add(self, user_id: int, sid: str, ttl_sec: int) -> None:
        k_user = self._user_key(user_id) 
        await self.r.sadd(k_user, sid) 
        await self.r.expire(k_user, ttl_sec) 
    
    async def contains(self, user_id: int, sid: str, ttl_sec: int = 0) -> bool:
        k_user = self._user_key(user_id)
        res = await self.r.sismember(k_user, sid)
        if res == 1 and ttl_sec > 0:
            await self.r.expire(k_user, ttl_sec, gt = True) 
        return res == 1
    
    async def remove(self, user_id: int, sid: str) -> None:
        await self.r.srem(self._user_key(user_id), sid)

    async def remove_all(self, user_id: int) -> None:
        await self.r.delete(self._user_key(user_id))
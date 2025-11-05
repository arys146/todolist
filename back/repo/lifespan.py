from contextlib import asynccontextmanager
from fastapi import FastAPI
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
import os
from redis import asyncio as aioredis

@asynccontextmanager
async def lifespan(app: FastAPI):
    engine = create_async_engine(os.getenv("DATABASE_URL"), pool_pre_ping=True)
    app.state.sessionmaker = async_sessionmaker(engine, expire_on_commit=False)
    redis = aioredis.from_url(os.getenv("REDIS_URL"), decode_responses=True)
    app.state.redis = redis
    try:
        yield
    finally:
        await engine.dispose()
        await app.state.redis.close()
from typing import AsyncGenerator
from services.user import UserService
from services.task import TaskService
from services.tag import TagService
from services.habbit import HabbitService
from services.list import ListService
from .sqlalchemy_uow import SQLAlchemyUnitOfWork
from .uow import UnitOfWork
from .db import get_session
from fastapi import Depends, Request
from .ramStorage import RamStorage
from .redisStorage import RedisStorage

async def provide_uow(session = Depends(get_session)) -> AsyncGenerator[UnitOfWork, None]:
    uow: UnitOfWork = SQLAlchemyUnitOfWork(session)
    try:
        yield uow
    finally:
        await uow.rollback()

def provide_ram_storage(request: Request) -> RamStorage:
    return RedisStorage(request.app.state.redis)
    

async def provide_user_service(uow = Depends(provide_uow), ramStorage = Depends(provide_ram_storage)) -> UserService:
    return UserService(uow, ramStorage)

async def provide_task_service(uow = Depends(provide_uow)) -> TaskService:
    return TaskService(uow)

async def provide_tag_service(uow = Depends(provide_uow)) -> TagService:
    return TagService(uow)

async def provide_habbit_service(uow = Depends(provide_uow)) -> HabbitService:
    return HabbitService(uow)

async def provide_list_service(uow = Depends(provide_uow)) -> ListService:
    return ListService(uow)


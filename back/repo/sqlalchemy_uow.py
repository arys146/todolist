from sqlalchemy.ext.asyncio import AsyncSession
from .uow import UnitOfWork
from .alchemyTaskRepo import SQLAlchemyTaskRepository
from .alchemyTagRepo import SQLAlchemyTagRepository
from .alchemyUserRepo import SQLAlchemyUserRepository
from .alchemyHabbitRepo import SQLAlchemyHabbitRepository
from .alchemyHabbitTrackerRepo import SQLAlchemyHabbitTrackerRepository
from .alchemyRefreshTokenRepo import SQLAlchemyRefreshTokenRepository

class SQLAlchemyUnitOfWork(UnitOfWork):
    def __init__(self, session: AsyncSession):
        self._session = session
        self._committed = False
        self.tasks = SQLAlchemyTaskRepository(session)
        self.tags = SQLAlchemyTagRepository(session)
        self.users = SQLAlchemyUserRepository(session)
        self.habbits = SQLAlchemyHabbitRepository(session)
        self.habbit_tracker = SQLAlchemyHabbitTrackerRepository(session)
        self.refresh_tokens = SQLAlchemyRefreshTokenRepository(session)

    def committed(self) -> bool:
        return self._committed

    async def commit(self) -> None: 
        await self._session.commit()
        self._committed = True


    async def __aenter__(self):
        self._committed = False
        return self

    async def __aexit__(self, exc_type, exc, tb):
        if exc_type:
            await self.rollback()
        elif not self._committed:
            await self.commit()

    async def rollback(self) -> None:
        if self._committed:
            return
        try:
            await self._session.rollback()
        except Exception as e:
            print(e)
            pass
from datetime import date
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert, delete
from models.habbit_tracker import HabbitTracker
from schemas.habbitCheck import HabbitTrackerCreate

class SQLAlchemyHabbitTrackerRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_day(self, create : HabbitTrackerCreate) -> HabbitTracker | None:
        stmt = select(HabbitTracker).where(
            HabbitTracker.habbit_id == create.habbit_id,
            HabbitTracker.logical_date == create.logical_date
        )
        res = await self.session.execute(stmt)
        return res.scalar_one_or_none()

    async def check(self, create : HabbitTrackerCreate) -> HabbitTracker:
        existing = await self.get_by_day(create)
        if existing:
            return existing
        ddata = create.model_dump()
        tr = HabbitTracker(**ddata)
        self.session.add(tr)
        await self.session.flush()
        await self.session.refresh(tr)
        return tr

    async def uncheck(self, create : HabbitTrackerCreate) -> int:
        stmt = delete(HabbitTracker).where(
            HabbitTracker.habbit_id == create.habbit_id,
            HabbitTracker.logical_date == create.logical_date
        )
        res = await self.session.execute(stmt)
        return res.rowcount or 0
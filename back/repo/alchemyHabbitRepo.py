from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from .habbitRepository import HabbitRepository  
from models.habbit import Habbit                
from schemas.habbit import HabbitCreate  

class SQLAlchemyHabbitRepository(HabbitRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_habbit_by_id(self, id: int) -> Habbit | None:
        stmt = select(Habbit).options(selectinload(Habbit.tags)).where(Habbit.id == id)    
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def create_habbit(self, data: HabbitCreate, user_id: int) -> Habbit | None:
        payload = data.model_dump(exclude={"tag_ids"})
        payload.update({"owner_id": user_id})

        habbit = Habbit(**payload)
        self.session.add(habbit)
        await self.session.flush()
        await self.session.refresh(habbit)
        return habbit
    
    async def get_habbits_by_user(self, user_id:int) -> list[Habbit]:
        stmt = select(Habbit).options(selectinload(Habbit.tags)).where(Habbit.owner_id==user_id)
        result = await self.session.execute(stmt)
        return result.scalars().all()
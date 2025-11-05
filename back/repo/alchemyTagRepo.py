from sqlalchemy.ext.asyncio import AsyncSession
from .tagRepository import TagRepository
from models.tag import Tag
from schemas.tag import TagCreate
from sqlalchemy import select

class SQLAlchemyTagRepository(TagRepository):
    def __init__(self, session : AsyncSession):
        self.session = session


    async def get_tag_by_id(self, id: int) -> Tag | None:
        stmt = select(Tag).where(Tag.id == id)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_tags_by_ids(self, ids: list[int]) -> list[Tag]:
        if not ids:
            return []
        stmt = select(Tag).where(Tag.id.in_(ids))
        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    async def create_tag(self, data: TagCreate, user_id: int) -> Tag | None:
        ddata = data.model_dump()
        ddata.update({"owner_id": user_id})
        tag = Tag(**ddata)
        self.session.add(tag)
        await self.session.flush()
        await self.session.refresh(tag)
        return tag
    
    async def get_all_tags(self, user_id: int) -> list[Tag]:
        stmt = select(Tag).where(Tag.owner_id == user_id)
        result = await self.session.execute(stmt)
        return list(result.scalars().all())
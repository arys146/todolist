from repo.uow import UnitOfWork
from schemas.tag import TagCreate, TagUpdate
from fastapi import HTTPException, Response, status
from models.user import User
from models.tag import Tag

class TagService:

    def __init__(self, uow: UnitOfWork):
        self.uow = uow


    async def get_all_tags(self, user: User) -> list[Tag]:
        async with self.uow:
            return await self.uow.tags.get_all_tags(user.id)

    async def create_tag(self, data: TagCreate, user: User) -> Tag|None:
        async with self.uow:
            tag = await self.uow.tags.create_tag(data, user.id)
            return tag
    
    async def update_tag(self, tag_id: int, data: TagUpdate, user: User) -> Tag | None:
        async with self.uow:
            tag = await self.uow.tags.get_tag_by_id(tag_id)

            if not tag or tag.owner_id != user.id:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tag not found")

            for key, value in data.model_dump(exclude_unset=True).items():
                setattr(tag, key, value)

            await self.uow.commit()
            return tag
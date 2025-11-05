from abc import ABC, abstractmethod
from models.tag import Tag
from schemas.tag import TagCreate

class TagRepository(ABC):
    @abstractmethod
    async def get_tag_by_id(self, id: int) -> Tag | None:
        pass

    @abstractmethod
    async def create_tag(self, data: TagCreate, user_id: int) -> Tag | None:
        pass

    @abstractmethod
    async def get_tags_by_ids(self, ids: list[int]) -> list[Tag]:
        pass

    @abstractmethod
    async def get_all_tags(self, user_id: int) -> list[Tag]:
        pass
from sqlalchemy.ext.asyncio import AsyncSession
from .userRepository import UserRepository
from models.user import User
from schemas.user import UserCreate
from sqlalchemy import select

class SQLAlchemyUserRepository(UserRepository):
    def __init__(self, session : AsyncSession):
        self.session = session


    async def get_user_by_id(self, id: int) -> User | None:
        stmt = select(User).where(User.id == id)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_user_by_username(self, username: str) -> User | None:
        stmt = select(User).where(User.username == username)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def create_user(self, data: UserCreate) -> User | None:
        user = User(**data.model_dump())
        self.session.add(user)
        await self.session.flush()
        await self.session.refresh(user)
        return user
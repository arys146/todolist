from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from .refreshTokenRepository import RefreshTokenRepository  
from models.refresh_token import RefreshToken                
from schemas.token import RefreshCreate  

class SQLAlchemyRefreshTokenRepository(RefreshTokenRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_token_by_hash(self, token_hash: str) -> RefreshToken | None:
        stmt = select(RefreshToken).where(RefreshToken.token_hash == token_hash)    
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def create_token(self, data: RefreshCreate) -> RefreshToken | None:
        payload = data.model_dump()

        token = RefreshToken(**payload)
        self.session.add(token)
        await self.session.flush()
        await self.session.refresh(token)
        return token
    
    async def get_token_by_user(self, user_id: int) -> list[RefreshToken]: 
        stmt = select(RefreshToken).where(RefreshToken.user_id==user_id)
        result = await self.session.execute(stmt)
        return result.scalars().all()
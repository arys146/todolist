from fastapi import Request
from sqlalchemy.ext.asyncio import AsyncSession
from typing import AsyncGenerator
import repo.init



async def get_session(request: Request) -> AsyncGenerator[AsyncSession, None]:
    Session = request.app.state.sessionmaker
    async with Session() as session:
        yield session
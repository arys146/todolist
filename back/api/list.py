from fastapi import APIRouter, Depends, HTTPException, Response, status
from services.list import ListService
from repo.provider import provide_list_service
from models.user import User
from middleware.auth import get_current_user_oauth2
from schemas.list import ListToday

def list_routes() -> APIRouter:
    router = APIRouter()
    
    @router.get("/list-today", response_model=ListToday)
    async def create_habbit(user: User = Depends(get_current_user_oauth2), service: ListService = Depends(provide_list_service)):
        return await service.for_today(user)

    
    return router
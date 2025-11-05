from fastapi import APIRouter, Depends, Response
from services.habbit import HabbitService
from models.user import User
from middleware.auth import get_current_user_oauth2
from repo.provider import provide_habbit_service
from schemas.habbit import HabbitCreate, HabbitRead, HabbitUpdate
from schemas.habbitCheck import HabbitTrackerSend

def habbit_routes() -> APIRouter:
    router = APIRouter()
    
    @router.post("/habit", response_model=HabbitRead)
    async def create_habbit(data: HabbitCreate, user: User = Depends(get_current_user_oauth2), service: HabbitService = Depends(provide_habbit_service)):
        return await service.create_habbit(data, user)
    
    @router.put("/habit/{habbit_id}", response_model=HabbitRead)
    async def update_habbit(habbit_id: int, data: HabbitUpdate, user: User = Depends(get_current_user_oauth2), service: HabbitService = Depends(provide_habbit_service)):
        return await service.update_habbit(habbit_id, data, user)

    @router.post("/habit-check")
    async def check_habbit(data: HabbitTrackerSend, user: User = Depends(get_current_user_oauth2), service: HabbitService = Depends(provide_habbit_service)):
        return await service.check_habbit(data, user)
    
    @router.post("/habit-uncheck")
    async def uncheck_habbit(data: HabbitTrackerSend, user: User = Depends(get_current_user_oauth2), service: HabbitService = Depends(provide_habbit_service)):
        return await service.uncheck_habbit(data, user)
    
    


    return router
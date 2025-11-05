from fastapi import APIRouter, Depends, Response
from services.tag import TagService
from models.user import User
from middleware.auth import get_current_user_oauth2
from repo.provider import provide_tag_service
from schemas.tag import TagCreate, TagRead, TagUpdate

def tag_routes() -> APIRouter:
    router = APIRouter()
    
    @router.post("/tag", response_model=TagRead)
    async def create_tag(data: TagCreate, user: User = Depends(get_current_user_oauth2), service: TagService = Depends(provide_tag_service)):
        return await service.create_tag(data, user)
    
    @router.put("/tag/{tag_id}", response_model=TagRead)
    async def update_tag(tag_id: int, data: TagUpdate, user: User = Depends(get_current_user_oauth2), service: TagService = Depends(provide_tag_service)):
        return await service.update_tag(tag_id, data, user)
    
    @router.get("/tags", response_model=list[TagRead])
    async def get_all_tags(user: User = Depends(get_current_user_oauth2), service: TagService = Depends(provide_tag_service)):
        return await service.get_all_tags(user)


    return router
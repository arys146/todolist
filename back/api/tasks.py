from fastapi import APIRouter, Depends, Response
from services.task import TaskService
from models.user import User
from middleware.auth import get_current_user_oauth2
from repo.provider import provide_task_service
from schemas.task import TaskCreate, TaskRead, TaskUpdate

def task_routes() -> APIRouter:
    router = APIRouter()
    
    @router.post("/task", response_model=TaskRead)
    async def create_task(data: TaskCreate, user: User = Depends(get_current_user_oauth2), service: TaskService = Depends(provide_task_service)):
        return await service.create_task(data, user)
    
    @router.put("/task/{task_id}", response_model=TaskRead)
    async def update_task(task_id: int, data: TaskUpdate, user: User = Depends(get_current_user_oauth2), service: TaskService = Depends(provide_task_service)):
        return await service.update_task(task_id, data, user)
    
    @router.put("/complete_task/{task_id}", response_model=TaskRead)
    async def complete_task(task_id: int, user: User = Depends(get_current_user_oauth2), service: TaskService = Depends(provide_task_service)):
        return await service.complete_task(task_id, user)
    
    @router.put("/uncomplete_task/{task_id}", response_model=TaskRead)
    async def uncomplete_task(task_id: int, user: User = Depends(get_current_user_oauth2), service: TaskService = Depends(provide_task_service)):
        return await service.uncomplete_task(task_id, user)


    return router
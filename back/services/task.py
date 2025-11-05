from repo.uow import UnitOfWork
from schemas.task import TaskCreate, TaskUpdate, FIELDS_TO_EXCLUDE
from fastapi import HTTPException, Response, status
from models.user import User
from models.task import Task
from sqlalchemy.orm import attributes

class TaskService:

    def __init__(self, uow: UnitOfWork):
        self.uow = uow

        
    async def create_task(self, data: TaskCreate, user: User) -> Task|None:
        async with self.uow:
            task = await self.uow.tasks.create_task(data, user.id)
            if data.tag_ids:
                tags = await self.uow.tags.get_tags_by_ids(data.tag_ids)
                attributes.set_committed_value(task, "tags", tags)
            return task
    
    async def update_task(self, task_id: int, data: TaskUpdate, user: User) -> Task | None:
        async with self.uow:
            task = await self.uow.tasks.get_task_by_id(task_id)

            if not task or task.owner_id != user.id:
                raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail="Task not found")

            for key, value in data.model_dump(exclude_unset=True, exclude=FIELDS_TO_EXCLUDE).items():
                setattr(task, key, value)
            
            tags = await self.uow.tags.get_tags_by_ids(data.tag_ids)
            task.tags = tags

            return task
        
    async def complete_task(self, task_id: int, user: User) -> Task | None:
        async with self.uow:
            task = await self.uow.tasks.get_task_by_id(task_id)

            if not task or task.owner_id != user.id:
                raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail="Task not found")

            task.status = True

            return task
        
    async def uncomplete_task(self, task_id: int, user: User) -> Task | None:
        async with self.uow:
            task = await self.uow.tasks.get_task_by_id(task_id)

            if not task or task.owner_id != user.id:
                raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail="Task not found")

            task.status = False

            return task
    
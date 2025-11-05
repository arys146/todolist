from sqlalchemy.ext.asyncio import AsyncSession
from .taskRepository import TaskRepository
from models.task import Task
from schemas.task import TaskCreate, TaskUpdate
from sqlalchemy import select
from sqlalchemy.orm import selectinload

class SQLAlchemyTaskRepository(TaskRepository):
    def __init__(self, session : AsyncSession):
        self.session = session


    async def get_task_by_id(self, id: int) -> Task | None:
        stmt = select(Task).options(selectinload(Task.tags)).where(Task.id == id)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def create_task(self, data: TaskCreate, user_id: int) -> Task | None:
        ddata = data.model_dump(exclude={"tag_ids"})
        ddata.update({"owner_id": user_id})
        task = Task(**ddata)
        self.session.add(task)
        await self.session.flush()
        await self.session.refresh(task)
        return task
    
    async def get_tasks_by_user(self, user_id:int) -> list[Task]:
        stmt = select(Task).options(selectinload(Task.tags)).where(Task.owner_id==user_id)
        result = await self.session.execute(stmt)
        return result.scalars().all()
    
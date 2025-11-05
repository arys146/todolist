from abc import ABC, abstractmethod
from models.task import Task
from schemas.task import TaskCreate

class TaskRepository(ABC):
    @abstractmethod
    async def get_task_by_id(self, id: int) -> Task | None:
        pass

    @abstractmethod
    async def create_task(self, data: TaskCreate, user_id: int) -> Task | None:
        pass

    @abstractmethod
    async def get_tasks_by_user(self, user_id:int) -> list[Task]:
        pass
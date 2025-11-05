# repo/uow.py
from abc import ABC, abstractmethod
from repo import tagRepository, userRepository, taskRepository, habbitRepository, habbitTrackerRepository, refreshTokenRepository
class UnitOfWork(ABC):
    tasks: taskRepository.TaskRepository
    tags: tagRepository.TagRepository
    users: userRepository.UserRepository
    habbits: habbitRepository.HabbitRepository
    habbit_tracker: habbitTrackerRepository.HabbitTrackerRepository
    refresh_tokens: refreshTokenRepository.RefreshTokenRepository

    @abstractmethod
    async def commit(self) -> None: pass
    @abstractmethod
    async def rollback(self) -> None: pass

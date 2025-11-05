from datetime import datetime
from helpers import parser
from helpers.logicalDate import get_logical_date
from repo.uow import UnitOfWork
from fastapi import HTTPException, Response, status
from models.user import User
from models.tag import Tag
from schemas.habbitCheck import HabbitTrackerCreate
from schemas.habbit import HabbitElement
from schemas.task import TaskRead
from schemas.list import ListToday

class ListService:

    def __init__(self, uow: UnitOfWork):
        self.uow = uow

        
    async def today_habbits(self, user : User) ->list[HabbitElement]:
            habbits = await self.uow.habbits.get_habbits_by_user(user.id)
            filtered = []
            log_day = get_logical_date(user.day_start_offset, datetime.now())
            for habbit in habbits:
                t, interval, values = parser.parse_string(habbit.schedule)
                if parser.is_today(t, interval, values, log_day, get_logical_date(user.day_start_offset, habbit.created_at)):
                    filtered.append(habbit)
            habbits = []
            for habbit in filtered:
                is_checked = await self.uow.habbit_tracker.get_by_day(HabbitTrackerCreate(habbit_id=habbit.id, logical_date=log_day)) is not None
                element = HabbitElement.model_validate(habbit)
                element.is_checked = is_checked
                habbits.append(element)
            return habbits
    
    async def all_tasks(self, user : User) -> list[TaskRead]:
            tasks = await self.uow.tasks.get_tasks_by_user(user.id)
            result = []
            for task in tasks:
                task_read = TaskRead.model_validate(task)
                result.append(task_read)
            result.sort(key=lambda p: p.due_date)
            return result
        
    async def for_today(self, user : User) -> ListToday:
        async with self.uow:
            habbits = await self.today_habbits(user)
            tasks = await self.all_tasks(user)
            return ListToday(habbits=habbits, tasks=tasks)
            
from datetime import date, datetime
from repo.uow import UnitOfWork
from schemas.habbit import HabbitCreate, HabbitUpdate, FIELDS_TO_EXCLUDE
from schemas.habbitCheck import HabbitTrackerCreate, HabbitTrackerSend
from fastapi import HTTPException, Response, status
from helpers.logicalDate import get_logical_date
from models.user import User
from models.habbit import Habbit
from models.habbit_tracker import HabbitTracker
from sqlalchemy.orm import attributes
from helpers import parser

class HabbitService:

    def __init__(self, uow: UnitOfWork):
        self.uow = uow

        
    async def create_habbit(self, data: HabbitCreate, user: User) -> Habbit|None:
        async with self.uow:
            habbit = await self.uow.habbits.create_habbit(data, user.id)
            if data.tag_ids:
                tags = await self.uow.tags.get_tags_by_ids(data.tag_ids)
                attributes.set_committed_value(habbit, "tags", tags)
            return habbit
    
    async def update_habbit(self, habbit_id: int, data: HabbitUpdate, user: User) -> Habbit | None:
        async with self.uow:
            habbit = await self.uow.habbits.get_habbit_by_id(habbit_id)

            if not habbit or habbit.owner_id != user.id:
                raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail="habit not found")

            for key, value in data.model_dump(exclude_unset=True, exclude=FIELDS_TO_EXCLUDE).items():
                setattr(habbit, key, value)
            
            tags = await self.uow.tags.get_tags_by_ids(data.tag_ids)
            habbit.tags = tags

            return habbit
        

    async def check_habbit(self, data: HabbitTrackerSend, user: User) -> HabbitTracker|None:
        async with self.uow:
            habbit = await self.uow.habbits.get_habbit_by_id(data.habit_id)
            if not habbit or habbit.owner_id != user.id:
                raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail="habit not found")
            
            log_day = get_logical_date(user.day_start_offset, datetime.now())
            t, interval, values = parser.parse_string(habbit.schedule)
            if not parser.is_today(t, interval, values, log_day, get_logical_date(user.day_start_offset, habbit.created_at)):
                raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST, detail="can't check habit today")

            ddata = HabbitTrackerCreate(habbit_id=habbit.id, logical_date=log_day)
            
            return await self.uow.habbit_tracker.check(ddata)
        

    async def uncheck_habbit(self, data: HabbitTrackerSend, user: User) -> int|None:
        async with self.uow:
            habbit = await self.uow.habbits.get_habbit_by_id(data.habit_id)
            if not habbit or habbit.owner_id != user.id:
                raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail="habit not found")
            
            ddata = HabbitTrackerCreate(habbit_id=habbit.id, logical_date=get_logical_date(user.day_start_offset, datetime.now()))
            
            return await self.uow.habbit_tracker.uncheck(ddata)
        
    
from datetime import date, datetime
from typing import List
from pydantic import BaseModel
from schemas.task import TaskRead
from schemas.habbit import HabbitElement


class ListToday(BaseModel):
    habbits: List[HabbitElement]
    tasks: List[TaskRead]

    model_config = {
        "from_attributes": True
    }
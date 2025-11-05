from datetime import date, datetime
from pydantic import BaseModel

class HabbitTrackerSend(BaseModel):
    habit_id: int

class HabbitTrackerCreate(BaseModel):
    habbit_id: int
    logical_date: date


class HabbitTrackerRead(BaseModel):
    id: int
    habit_id: int
    date: date

    model_config = {
        "from_attributes": True
    }

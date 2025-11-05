from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field
from schemas.tag import TagRead

FIELDS_TO_EXCLUDE = {"tag_ids"}
MIN_PRIORITY = 1
MAX_PRIORITY = 10

class TaskCreate(BaseModel):
    title:str
    description:Optional[str] = None
    priority: int = Field(..., ge = MIN_PRIORITY, le = MAX_PRIORITY)
    due_date: Optional[datetime] = None
    tag_ids: Optional[List[int]] = []

class TaskRead(BaseModel):
    id: int
    title: str
    description: str
    priority: int
    tags: List[TagRead]
    due_date: datetime
    status: bool
    model_config = {
        "from_attributes": True
    }

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    due_date: Optional[datetime] = None
    priority: int = Field(..., ge = MIN_PRIORITY, le = MAX_PRIORITY)
    status: Optional[bool] = None
    tag_ids: Optional[List[int]] = []
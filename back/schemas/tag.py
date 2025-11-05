from typing import Optional, List
from pydantic import BaseModel, Field

class TagCreate(BaseModel):
    title:str
    color:str

class TagUpdate(BaseModel):
    id: int
    title: Optional[str] = None
    color: Optional[str] = None

class TagRead(BaseModel):
    id: int
    title:str
    color:str

    model_config = {
        "from_attributes": True
    }

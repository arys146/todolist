from pydantic import BaseModel, Field
from typing import Optional
from datetime import time



class UserCreate(BaseModel):
    username: str = Field(..., min_length=3, max_length=25, pattern=r'^[a-zA-Z0-9_]+$')
    name: str = Field(..., min_length=3, max_length=25)
    password: str = Field(..., min_length=3, pattern=r'^[a-zA-Z0-9!@#$%^&*()_+\-=\[\]{};:\'",.<>/?\\|`~]+$')
    day_start_offset: Optional[time] = None


class UserLogin(BaseModel):
    username: str = Field(..., min_length=3, max_length=25, pattern=r'^[a-zA-Z0-9_]+$')
    password: str = Field(..., min_length=3, pattern=r'^[a-zA-Z0-9!@#$%^&*()_+\-=\[\]{};:\'",.<>/?\\|`~]+$')


class UserRead(BaseModel):
    id: int
    username: str
    name: str

    model_config = {
        "from_attributes": True
    }

class UserLoginResponce(BaseModel):
    user: UserRead
    access_token: str 

    model_config = {
        "from_attributes": True
    }






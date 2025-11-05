from typing import Optional
from pydantic import BaseModel, Field

class Error(BaseModel):
    msg:str

    model_config = {
        "from_attributes": True
    }
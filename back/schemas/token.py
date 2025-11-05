from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field


class RefreshCreate(BaseModel):
    token_hash: str
    user_id: int
    sid: str
    issued_at: datetime
    expires_at: datetime
    revoked: bool
    device_name: Optional[str] = None

class AccessEncode(BaseModel):
    user_id: int
    sid: str

class RefreshResponce(BaseModel):
    access_token: str

    model_config = {
        "from_attributes": True
    }
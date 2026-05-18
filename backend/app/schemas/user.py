from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime

class UserCreate(BaseModel):
    username: str
    full_name: Optional[str] = None
    uid_nfc: Optional[str] = None
    role: str = "viewer"

class UserResponse(UserCreate):
    id: int
    is_active: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
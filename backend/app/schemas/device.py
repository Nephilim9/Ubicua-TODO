from pydantic import BaseModel, ConfigDict, Field
from typing import Optional
from datetime import datetime

class DeviceBase(BaseModel):
    name: str
    location: Optional[str] = None
    device_type: str = Field(..., pattern="^(MASTER|SLAVE)$")

class DeviceCreate(DeviceBase):
    mac_address: str = Field(..., pattern="^([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})$")

class DeviceUpdate(BaseModel):
    name: Optional[str] = None
    location: Optional[str] = None
    status: Optional[str] = Field(None, pattern="^(online|offline|error)$")
    firmware_version: Optional[str] = None

class DeviceResponse(DeviceCreate):
    id: int
    status: str
    last_seen: Optional[datetime] = None
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)
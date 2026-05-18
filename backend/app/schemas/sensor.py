from pydantic import BaseModel, ConfigDict, Field
from typing import Optional
from datetime import datetime

class SensorBase(BaseModel):
    sensor_type: str = Field(..., pattern="^(MQ135|PIR|NFC|TEMP|HUMIDITY)$")
    pin_number: Optional[int] = None
    name: str
    unit: Optional[str] = None
    is_active: bool = True

class SensorCreate(SensorBase):
    device_id: int

class SensorUpdate(BaseModel):
    name: Optional[str] = None
    is_active: Optional[bool] = None
    unit: Optional[str] = None

class SensorResponse(SensorCreate):
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
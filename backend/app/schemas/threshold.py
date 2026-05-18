from pydantic import BaseModel, ConfigDict, Field
from typing import Optional, List
from datetime import datetime

class ThresholdBase(BaseModel):
    sensor_type: str
    name: str
    operator: str = Field(..., pattern="^(GT|LT|EQ|BETWEEN)$")
    value_min: Optional[float] = None
    value_max: Optional[float] = None
    severity: str = Field(..., pattern="^(LOW|MEDIUM|HIGH|CRITICAL)$")
    is_active: bool = True
    notification_channels: str = '["ws"]'

class ThresholdCreate(ThresholdBase):
    pass

class ThresholdUpdate(BaseModel):
    name: Optional[str] = None
    value_min: Optional[float] = None
    value_max: Optional[float] = None
    severity: Optional[str] = None
    is_active: Optional[bool] = None

class ThresholdResponse(ThresholdBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)
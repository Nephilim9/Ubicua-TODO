from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime

class AlertUpdate(BaseModel):
    status: str # 'acknowledged' o 'resolved'
    resolved_by: Optional[str] = None

class AlertResponse(BaseModel):
    id: int
    sensor_id: Optional[int]
    device_id: Optional[int]
    threshold_id: Optional[int]
    severity: str
    message: str
    value_triggered: float
    status: str
    created_at: datetime
    resolved_at: Optional[datetime] = None
    resolved_by: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)
from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime

class ReadingCreate(BaseModel):
    sensor_id: int
    device_id: int
    value: float
    value_processed: Optional[float] = None

class ReadingResponse(ReadingCreate):
    id: int
    timestamp: datetime

    model_config = ConfigDict(from_attributes=True)
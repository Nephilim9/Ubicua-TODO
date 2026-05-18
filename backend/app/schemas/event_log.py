from pydantic import BaseModel, ConfigDict
from datetime import datetime

class EventLogResponse(BaseModel):
    id: int
    event_type: str
    source: str
    payload: str
    level: str
    timestamp: datetime

    model_config = ConfigDict(from_attributes=True)
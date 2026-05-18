from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from app.database import Base

class EventLog(Base):
    __tablename__ = "event_logs"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    event_type = Column(String, nullable=False, index=True)
    source = Column(String, nullable=False)
    payload = Column(String) # Almacenado como JSON string
    level = Column(String, server_default='INFO', index=True) # DEBUG, INFO, WARNING, ERROR, CRITICAL
    timestamp = Column(DateTime(timezone=True), server_default=func.now(), index=True)
from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base

class Threshold(Base):
    __tablename__ = "thresholds"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    sensor_type = Column(String, nullable=False)
    name = Column(String, nullable=False)
    operator = Column(String) # 'GT', 'LT', 'EQ', 'BETWEEN'
    value_min = Column(Float)
    value_max = Column(Float)
    severity = Column(String) # 'LOW', 'MEDIUM', 'HIGH', 'CRITICAL'
    is_active = Column(Boolean, server_default=text("1"))
    notification_channels = Column(String) # Almacenado como JSON string
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relaciones
    alerts = relationship("Alert", back_populates="threshold")
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime, text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base

class Sensor(Base):
    __tablename__ = "sensors"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    device_id = Column(Integer, ForeignKey("devices.id", ondelete="CASCADE"))
    sensor_type = Column(String, nullable=False) # 'MQ135', 'PIR', 'NFC', etc.
    pin_number = Column(Integer)
    name = Column(String, nullable=False)
    unit = Column(String)
    is_active = Column(Boolean, server_default=text("1"))
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relaciones
    device = relationship("Device", back_populates="sensors")
    readings = relationship("Reading", back_populates="sensor", cascade="all, delete-orphan")
    alerts = relationship("Alert", back_populates="sensor")
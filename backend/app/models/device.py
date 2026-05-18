from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base

class Device(Base):
    __tablename__ = "devices"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    mac_address = Column(String, unique=True, nullable=False, index=True)
    name = Column(String, nullable=False)
    location = Column(String)
    device_type = Column(String) # 'MASTER' o 'SLAVE'
    status = Column(String, server_default='offline')
    last_seen = Column(DateTime(timezone=True))
    firmware_version = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relaciones
    sensors = relationship("Sensor", back_populates="device", cascade="all, delete-orphan")
    alerts = relationship("Alert", back_populates="device")
    readings = relationship("Reading", back_populates="device")
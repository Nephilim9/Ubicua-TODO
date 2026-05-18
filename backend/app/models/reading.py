from sqlalchemy import Column, Integer, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base

class Reading(Base):
    __tablename__ = "readings"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    sensor_id = Column(Integer, ForeignKey("sensors.id", ondelete="CASCADE"))
    device_id = Column(Integer, ForeignKey("devices.id", ondelete="CASCADE"))
    value = Column(Float, nullable=False)
    value_processed = Column(Float)
    
    # Índice en timestamp es crucial para gráficas en tiempo real en la RPi
    timestamp = Column(DateTime(timezone=True), server_default=func.now(), index=True)

    # Relaciones
    sensor = relationship("Sensor", back_populates="readings")
    device = relationship("Device", back_populates="readings")
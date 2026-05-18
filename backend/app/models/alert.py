from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base

class Alert(Base):
    __tablename__ = "alerts"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    sensor_id = Column(Integer, ForeignKey("sensors.id", ondelete="SET NULL"), nullable=True)
    device_id = Column(Integer, ForeignKey("devices.id", ondelete="SET NULL"), nullable=True)
    threshold_id = Column(Integer, ForeignKey("thresholds.id", ondelete="SET NULL"), nullable=True)
    severity = Column(String, nullable=False)
    message = Column(String, nullable=False)
    value_triggered = Column(Float)
    status = Column(String, server_default='active', index=True) # active, resolved, acknowledged
    resolved_at = Column(DateTime(timezone=True))
    resolved_by = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), index=True)

    # Relaciones
    sensor = relationship("Sensor", back_populates="alerts")
    device = relationship("Device", back_populates="alerts")
    threshold = relationship("Threshold", back_populates="alerts")
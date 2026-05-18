from sqlalchemy import Column, Integer, String, Boolean, DateTime, text
from sqlalchemy.sql import func
from app.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    uid_nfc = Column(String, unique=True, index=True)
    username = Column(String, unique=True, nullable=False, index=True)
    full_name = Column(String)
    role = Column(String, server_default='viewer') # admin, operator, viewer
    is_active = Column(Boolean, server_default=text("1"))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
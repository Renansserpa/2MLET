from datetime import datetime
from sqlalchemy import Column, String, Integer, func, DateTime
from app.core.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    password = Column(String(255))
    email = Column(String(255))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
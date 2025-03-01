from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.sql import func
from .database import Base

class Model(Base):
    __tablename__ = "models"

    id = Column(String, primary_key=True, index=True)
    name = Column(String, index=True)
    version = Column(String, index=True)
    accuracy = Column(Float)
    file_path = Column(String)
    created_at = Column(DateTime(timezone=True), default=func.now())
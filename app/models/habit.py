from sqlalchemy import Column, Integer, String, JSON
from sqlalchemy.orm import relationship
from core.database import Base


class Habit(Base):
    __tablename__ = "habits"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    frequency = Column(JSON, nullable=True)
    #is_active = Column(Boolean, default=True)
    
    records = relationship("Record", back_populates="habit")

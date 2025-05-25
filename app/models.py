from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, func, JSON, Boolean
from sqlalchemy.orm import  relationship, declarative_base

Base = declarative_base()

class Habit(Base):
    __tablename__ = "habits"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    frequency = Column(JSON, nullable=True)
    records = relationship("Record", back_populates="habit")
    #is_active = Column(Boolean, default=True)

class Record(Base):
    __tablename__ = "records"
    id = Column(Integer, primary_key=True, index=True)
    habit_id = Column(Integer, ForeignKey("habits.id"))
    timestamp = Column(DateTime, default=func.now())
    habit = relationship("Habit", back_populates="records")
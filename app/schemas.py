from pydantic import BaseModel, Field, field_validator
from typing import Optional, List

# Schemas
class HabitCreate(BaseModel):
    name: str
    frequency: List[str] = Field(default_factory=lambda: ["Mo", "Tu", "We", "Th", "Fr", "Sa", "Su"])

    @field_validator("frequency")
    @classmethod
    def validate_frequency(cls, v):
        valid_days = {"Mo", "Tu", "We", "Th", "Fr", "Sa", "Su"}
        if not all(day in valid_days for day in v):
            raise ValueError(f"Dias inválidos. Valores válidos: {list(valid_days)}")
        return v


class HabitResponse(BaseModel):
    id: int
    name: str
    frequency: Optional[List[str]]

    class Config:
        from_attributes = True

class RecordCreate(BaseModel):
    habit_id: int

class RecordResponse(BaseModel):
    id: int
    habit_id: int
    timestamp: str

    class Config:
        from_attributes = True
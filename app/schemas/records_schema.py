from pydantic import BaseModel, Field, field_validator
from typing import Optional, List


class RecordCreate(BaseModel):
    habit_id: int

class RecordResponse(BaseModel):
    id: int
    habit_id: int
    timestamp: str

    class Config:
        from_attributes = True
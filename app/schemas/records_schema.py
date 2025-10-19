from pydantic import BaseModel, Field, field_validator
from typing import Optional, List


class RecordCreate(BaseModel):
    habit_id: int

class RecordResponse(BaseModel):
    message: str

    class Config:
        from_attributes = True

class RecordDetail(BaseModel):
    id: int
    habit_id: int
    timestamp: str

    class Config:
        from_attributes = True
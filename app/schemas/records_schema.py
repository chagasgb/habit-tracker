from datetime import datetime
from pydantic import BaseModel

class RecordCreate(BaseModel):
    habit_id: int

class RecordResponse(BaseModel):
    id: int
    habit_id: int
    timestamp: datetime

    class Config:
        from_attributes = True

from sqlalchemy.orm import Session
from fastapi import HTTPException
from models import Record
from crud.base import CRUDBase
from sqlalchemy import func

#epa
class RecordService:
    @staticmethod
    def create(db: Session, habit_id: int):
        record_crud = CRUDBase(Record)
        existing_record = (
            db.query(Record)
            .filter(Record.habit_id == habit_id)
            .filter(func.date(Record.timestamp) == func.date(func.now()))
            .first()
        )
        if existing_record:
            raise HTTPException(status_code=400, detail="Já existe um registro para este hábito hoje")
        return record_crud.create(db, {"habit_id": habit_id})

    @staticmethod
    def get_all(db: Session):
        record_crud = CRUDBase(Record)
        return record_crud.get_all(db)
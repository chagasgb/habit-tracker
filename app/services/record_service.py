from sqlalchemy.orm import Session
from fastapi import HTTPException
from models.record import Record
from models.habit import Habit
from services.record_crud import RecordCRUD
from sqlalchemy import func

class RecordService:
    def __init__(self, db: Session):
        self.db = db
        self.record_crud = RecordCRUD(db)

    def create(self, habit_id: int):
        # Verificar se o hábito existe
        habit = self.db.query(Habit).filter(Habit.id == habit_id).first()
        if not habit:
            raise HTTPException(status_code=404, detail="Hábito não encontrado")
        
        existing_record = self.record_crud.get_today_by_habit_id(habit_id)
        if existing_record:
            raise HTTPException(status_code=400, detail="Já existe um registro para este hábito hoje")
        return self.record_crud.create(habit_id)

    def get_all(self):
        return self.record_crud.get_all()

    def get_by_habit_id(self, habit_id: int):
        return self.record_crud.get_by_habit_id(habit_id)
    
    def delete(self, record_id: int):
        return self.record_crud.delete(record_id)
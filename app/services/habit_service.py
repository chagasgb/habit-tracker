from sqlalchemy.orm import Session
from fastapi import HTTPException
from models import Habit  
from crud.base import CRUDBase
from schemas.habits_schema import HabitCreate, HabitResponse  
import datetime

class HabitService:
    @staticmethod
    def create(db: Session, habit_data: HabitCreate):
        if db.query(Habit).filter(Habit.name == habit_data.name).first():
            raise HTTPException(status_code=400, detail="Hábito já existe")
        
        habit_crud = CRUDBase(Habit)
        return habit_crud.create(db, habit_data.model_dump())

    @staticmethod
    def get_all(db: Session):
        habit_crud = CRUDBase(Habit)
        habits = habit_crud.get_all(db)
        return [HabitResponse(**habit.__dict__) for habit in habits]

    @staticmethod
    def delete_by_id(db: Session, habit_id: int):
        habit = db.query(Habit).filter(Habit.id == habit_id).first()

        if not habit:
            raise HTTPException(status_code=404, detail="Hábito não encontrado")

        db.delete(habit)
        db.commit()
        return habit

    @staticmethod
    def get_scheduled_habits_db(db: Session, target_date: datetime.datetime):
        """
        Obtém os hábitos agendados para uma data específica.

        Parâmetros:
        - db: Sessão do banco de dados.
        - target_date: Objeto datetime.datetime representando a data alvo.

        O padrão do objeto datetime.datetime é:
        - Formato: YYYY-MM-DD HH:MM:SS
        - Exemplo: 2023-03-15 14:30:00
        """
        WEEKDAY_TO_ABBR = {
            0: "Mo", 1: "Tu", 2: "We", 3: "Th", 4: "Fr", 5: "Sa", 6: "Su"
        }
        habit_crud = CRUDBase(Habit)
        habits = habit_crud.get_all(db)
        
        
        scheduled_habits = []
        target_weekday_abbr = WEEKDAY_TO_ABBR[target_date.weekday()]
        
        for habit in habits:
            if habit.frequency and isinstance(habit.frequency, list):
                days = habit.frequency
                if target_weekday_abbr in days:
                    scheduled_habits.append({
                        "id": habit.id,
                        "name": habit.name,
                        "frequency": habit.frequency
                    })
        return scheduled_habits
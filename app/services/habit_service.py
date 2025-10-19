from sqlalchemy.orm import Session
from fastapi import HTTPException
from models.habit import Habit  
from services.habit_crud import HabitCRUD
from schemas.habits_schema import HabitCreate, HabitResponse  
import datetime


class HabitService:
    def __init__(self, db: Session):
        self.db = db
        self.habit_crud = HabitCRUD(db)

    def create(self, habit_data: HabitCreate):
        if self.habit_crud.get_by_name(habit_data.name):
            raise HTTPException(status_code=400, detail="Hábito já existe")
        
        return self.habit_crud.create(
            name=habit_data.name, 
            frequency=habit_data.frequency
        )

    def get_all(self):
        habits = self.habit_crud.get_all()
        return [HabitResponse(**habit.__dict__) for habit in habits]

    def delete_by_id(self, habit_id: int):
        habit = self.habit_crud.get_by_id(habit_id)

        if not habit:
            raise HTTPException(status_code=404, detail="Hábito não encontrado")

        return self.habit_crud.delete(habit_id)

    def get_scheduled_habits_db(self, target_date: datetime.datetime):
        """
        Obtém os hábitos agendados para uma data específica.

        Parâmetros:
        - target_date: Objeto datetime.datetime representando a data alvo.

        O padrão do objeto datetime.datetime é:
        - Formato: YYYY-MM-DD HH:MM:SS
        - Exemplo: 2023-03-15 14:30:00
        """
        WEEKDAY_TO_ABBR = {0: "Mo", 1: "Tu", 2: "We", 3: "Th", 4: "Fr", 5: "Sa", 6: "Su"}
        habits = self.habit_crud.get_all()
        
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
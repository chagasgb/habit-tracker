import datetime
from fastapi import APIRouter, Depends, HTTPException
from schemas.habits_schema import HabitCreate, HabitResponse
from services.habit_service import HabitService
from core.database import get_db
from sqlalchemy.orm import Session
from typing import List

router = APIRouter()

@router.post("")
def create_habit(habit: HabitCreate, db: Session = Depends(get_db)):
    service = HabitService(db)
    return service.create(habit)

@router.get("", response_model=List[HabitResponse])
def get_habits(db: Session = Depends(get_db)):
    service = HabitService(db)
    return service.get_all()
    
@router.delete("/{habit_id}")
def delete_habit(habit_id: int, db: Session = Depends(get_db)):
    service = HabitService(db)
    habit = service.delete_by_id(habit_id)
    return {
        "detail": f"Hábito '{habit.name}' (id {habit.id}) deletado com sucesso"
    }

@router.get("/scheduled", response_model=list)
def get_scheduled_habits(date: str, db: Session = Depends(get_db)):
    try:
        target_date = datetime.datetime.strptime(date, "%Y-%m-%d")
    except ValueError:
        raise HTTPException(status_code=400, detail="Formato de data inválido. Use YYYY-MM-DD")

    service = HabitService(db)
    scheduled_habits = service.get_scheduled_habits_db(target_date)
    return [HabitResponse(**habit) for habit in scheduled_habits]


##https://chatgpt.com/c/68c47411-8c48-8329-b1d0-b906359132f4
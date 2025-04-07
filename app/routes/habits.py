import datetime
from fastapi import APIRouter, Depends, HTTPException
from schemas import HabitCreate, HabitResponse
from services.habit_service import HabitService
from database import get_db
from sqlalchemy.orm import Session
from typing import List

router = APIRouter()

@router.post("")
def create_habit(habit: HabitCreate, db: Session = Depends(get_db)):
    return HabitService.create(db, habit)

@router.get("", response_model=List[HabitResponse])
def get_habits(db: Session = Depends(get_db)):
    habits = HabitService.get_all(db)
    return habits

@router.get("/scheduled", response_model=list)
def get_scheduled_habits(date: str, db: Session = Depends(get_db)):
    try:
        # Converter a string de data para um objeto datetime
        target_date = datetime.datetime.strptime(date, "%Y-%m-%d")
    except ValueError:
        raise HTTPException(status_code=400, detail="Formato de data inválido. Use YYYY-MM-DD")
    
    # Chamar o método da HabitService
    scheduled_habits = HabitService.get_scheduled_habits_db(db, target_date)
    
    # Converter os dicionários retornados para HabitResponse    
    return [HabitResponse(**habit) for habit in scheduled_habits]
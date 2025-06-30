import datetime
from fastapi import APIRouter, Depends, HTTPException
from schemas.habits_schema import HabitCreate, HabitResponse
from services.habit_service import HabitService
from database import get_db
from sqlalchemy.orm import Session
from typing import List

router = APIRouter()

@router.post("")
def create_habit(habit: HabitCreate, db: Session = Depends(get_db)):
    return HabitService.create(db, habit)

#@router.post("")
#def create_habits(habits: List[HabitCreate], db: Session = Depends(get_db)):
#    created = []
#    for habit in habits:
#        created.append(HabitService.create(db, habit))
#    return created

@router.get("", response_model=List[HabitResponse])
def get_habits(db: Session = Depends(get_db)):
    habits = HabitService.get_all(db)
    return habits

@router.delete("/{habit_id}")
def delete_habit(habit_id: int, db: Session = Depends(get_db)):
    habit = HabitService.delete_by_id(db, habit_id)
    return {
        "detail": f"Hábito '{habit.name}' (id {habit.id}) deletado com sucesso"
    }


@router.get("/scheduled", response_model=list)
def get_scheduled_habits(date: str, db: Session = Depends(get_db)):
    try:
        target_date = datetime.datetime.strptime(date, "%Y-%m-%d")
    except ValueError:
        raise HTTPException(status_code=400, detail="Formato de data inválido. Use YYYY-MM-DD")

    scheduled_habits = HabitService.get_scheduled_habits_db(db, target_date)
    return [HabitResponse(**habit) for habit in scheduled_habits]
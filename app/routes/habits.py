import datetime
from sqlalchemy.orm import Session
from typing import List
from fastapi import APIRouter, Depends

from dependencies import get_habit_service
from schemas.habits_schema import HabitCreate, HabitResponse
from schemas.common import MessageResponse
from services.habit_service import HabitService
from core.database import get_db

router = APIRouter()

@router.post("", response_model=HabitResponse, status_code=201)
def create_habit(habit: HabitCreate, service: HabitService = Depends(get_habit_service)) -> HabitResponse:
    return service.create(habit)

@router.get("", response_model=List[HabitResponse])
def get_habits(service: HabitService = Depends(get_habit_service)) -> list[HabitResponse]:
    return service.get_all()

@router.get("/scheduled", response_model=List[HabitResponse])
def get_scheduled_habits(date: datetime.date, service: HabitService = Depends(get_habit_service)) -> list[HabitResponse]:
    return service.get_scheduled_habits_db(date)

@router.delete("/{habit_id}", response_model=MessageResponse)
def delete_habit(habit_id: int, service: HabitService = Depends(get_habit_service)) -> MessageResponse:
    service.delete_by_id(habit_id)
    return MessageResponse(detail="Hábito deletado com sucesso")
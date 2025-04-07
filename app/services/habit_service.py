from sqlalchemy.orm import Session
from fastapi import HTTPException
from models import Habit  # Import do modelo
from crud.base import CRUDBase
from schemas import HabitCreate, HabitResponse  # Import dos schemas
from typing import List
import datetime
import logging

# Configurar logging básico
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

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
    def get_scheduled_habits_db(db: Session, target_date: datetime.datetime):
        WEEKDAY_TO_ABBR = {
            0: "Mo", 1: "Tu", 2: "We", 3: "Th", 4: "Fr", 5: "Sa", 6: "Su"
        }
        habit_crud = CRUDBase(Habit)
        habits = habit_crud.get_all(db)
        
        logger.debug(f"Total de hábitos no banco: {len(habits)}")
        for habit in habits:
            logger.debug(f"Hábito: {habit.name}, Frequency: {habit.frequency}")
        
        scheduled_habits = []
        target_weekday_abbr = WEEKDAY_TO_ABBR[target_date.weekday()]
        logger.debug(f"Dia alvo: {target_date}, Abreviação: {target_weekday_abbr}")
        
        for habit in habits:
            if habit.frequency and isinstance(habit.frequency, list):
                days = habit.frequency  # frequency é uma lista diretamente
                logger.debug(f"Verificando hábito '{habit.name}' com days: {days}")
                if target_weekday_abbr in days:
                    logger.debug(f"Hábito '{habit.name}' agendado para {target_weekday_abbr}")
                    scheduled_habits.append({
                        "id": habit.id,
                        "name": habit.name,
                        "frequency": habit.frequency
                    })
            else:
                logger.debug(f"Hábito '{habit.name}' sem frequency válido: {habit.frequency}")
        
        logger.debug(f"Hábitos agendados encontrados: {len(scheduled_habits)}")
        return scheduled_habits
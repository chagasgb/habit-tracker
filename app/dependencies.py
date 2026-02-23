# dependencies.py
from core.db_dependencies import DBSession
from services.habit_service import HabitService
from services.record_service import RecordService

def get_habit_service(db: DBSession) -> HabitService:
    return HabitService(db)

def get_record_service(db: DBSession) -> RecordService:
    return RecordService(db)

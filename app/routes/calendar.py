from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
import datetime

from core.database import get_db
from services.calendar_service import CalendarService

router = APIRouter(
    prefix="/calendar",
    tags=["Calendar"]
)

def get_calendar_service(db: Session = Depends(get_db)) -> CalendarService:
    return CalendarService(db)


@router.get("/range")
def get_calendar_range(
    center: datetime.date = Query(..., description="Dia central do range"),
    days_before: int = Query(0, description="Quantos dias antes do center incluir"),
    days_after: int = Query(0, description="Quantos dias depois do center incluir"),
    service: CalendarService = Depends(get_calendar_service),
):
    """
    Retorna uma lista de dias consecutivos incluindo o dia central.

    Ex:
    GET /calendar/range?center=2026-01-11&days_before=30&days_after=30
    """
    return service.get_range(center=center, days_before=days_before, days_after=days_after)

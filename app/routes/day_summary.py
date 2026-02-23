import datetime
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from core.database import get_db
from services.day_summary_service import DaySummaryService


router = APIRouter(prefix="/day-summary", tags=["Day Summary"])


def get_day_summary_service(db: Session = Depends(get_db)) -> DaySummaryService:
    return DaySummaryService(db)


@router.get("")
def get_day_summary(
    date: datetime.date,
    service: DaySummaryService = Depends(get_day_summary_service),
):
    """
    Retorna o resumo de um único dia.

    Ex:
    GET /day-summary?date=2026-01-10
    """
    return service.get_day_summary(date)

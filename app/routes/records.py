from typing import List, Optional

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from core.database import get_db
from schemas.records_schema import RecordResponse, RecordCreate
from dependencies import get_record_service
from schemas.common import MessageResponse
from services.record_service import RecordService

router = APIRouter()


@router.post("", response_model=RecordResponse, status_code=201)
def create_record(record: RecordCreate, service: RecordService = Depends(get_record_service)) -> RecordResponse:
    return service.create(record.habit_id)


# endpoint para obter registros, com filtro opcional por habit_id (...?habit_id=int)
@router.get("", response_model=List[RecordResponse])
def get_records(habit_id: Optional[int] = Query(None), service: RecordService = Depends(get_record_service)) -> List[RecordResponse]:
    if habit_id is not None:
        return service.get_by_habit_id(habit_id)
    return service.get_all()


@router.delete("/{record_id}", response_model=MessageResponse)
def delete_record(record_id: int, service: RecordService = Depends(get_record_service)) -> MessageResponse:
    record = service.delete(record_id)
    return MessageResponse(
        detail=f"Registro {record.id} deletado com sucesso"
    )


from fastapi import APIRouter, Depends, HTTPException, Query
from services.record_service import RecordService
from core.database import get_db
from sqlalchemy.orm import Session
from typing import Optional

from schemas.records_schema import RecordCreate, RecordResponse, RecordDetail

router = APIRouter()

@router.post("/", response_model=RecordResponse)
def create_record(record: RecordCreate, db: Session = Depends(get_db)):
    try:
        service = RecordService(db)
        record_obj = service.create(record.habit_id)
        return RecordResponse(message=f"Registro para o hábito {record_obj.habit_id} criado com sucesso")
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/", response_model=list[RecordDetail])
def get_records(habit_id: Optional[int] = Query(None), db: Session = Depends(get_db)):
    service = RecordService(db)
    if habit_id:
        records = service.get_by_habit_id(habit_id)
    else:
        records = service.get_all()
    return [RecordDetail(id=record.id, habit_id=record.habit_id, timestamp=record.timestamp.isoformat()) for record in records]

@router.delete("/{record_id}")
def delete_record(record_id: int, db: Session = Depends(get_db)):
    try:
        service = RecordService(db)
        record = service.delete(record_id)
        if not record:
            raise HTTPException(status_code=404, detail="Registro não encontrado")
        return {"message": f"Registro {record_id} deletado com sucesso"}
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
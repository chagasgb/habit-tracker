from fastapi import APIRouter, Depends, HTTPException
from services.record_service import RecordService
from database import get_db
from sqlalchemy.orm import Session


from schemas.records_schema import RecordCreate, RecordResponse

router = APIRouter()

@router.post("/", response_model=RecordResponse)
def create_record(record: RecordCreate, db: Session = Depends(get_db)):
    try:
        record_obj = RecordService.create(db, record.habit_id)
        return RecordResponse(message=f"Registro para o hábito {record_obj.habit_id} criado com sucesso")
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/", response_model=list)
def get_records(db: Session = Depends(get_db)):
    records = RecordService.get_all(db)
    return [{"id": record.id, "habit_id": record.habit_id, "timestamp": record.timestamp.isoformat()} for record in records]
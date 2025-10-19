from sqlalchemy.orm import Session
from models.record import Record


class RecordCRUD:
    def __init__(self, db: Session):
        self.db = db

    def create(self, habit_id: int) -> Record:
        record = Record(habit_id=habit_id)
        self.db.add(record)
        self.db.commit()
        self.db.refresh(record)
        return record

    def get_by_id(self, record_id: int) -> Record | None:
        return self.db.query(Record).filter(Record.id == record_id).first()

    def get_all(self) -> list[Record]:
        return self.db.query(Record).all()

    def delete(self, record_id: int) -> Record | None:
        record = self.get_by_id(record_id)
        if record:
            self.db.delete(record)
            self.db.commit()
        return record

    def get_by_habit_id(self, habit_id: int) -> list[Record]:
        return self.db.query(Record).filter(Record.habit_id == habit_id).all()

    def get_today_by_habit_id(self, habit_id: int) -> Record | None:
        from sqlalchemy import func
        return (
            self.db.query(Record)
            .filter(Record.habit_id == habit_id)
            .filter(func.date(Record.timestamp) == func.date(func.now()))
            .first()
        )

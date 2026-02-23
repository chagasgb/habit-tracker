from sqlalchemy.orm import Session
from models.habit import Habit
from models.record import Record

class HabitCRUD:
    def __init__(self, db: Session):
        self.db = db

    def create(self, name: str, frequency=None) -> Habit:
        habit = Habit(name=name, frequency=frequency)
        self.db.add(habit)
        self.db.commit()
        self.db.refresh(habit)
        return habit

    def delete(self, habit_id: int) -> Habit | None:
        habit = self.get_by_id(habit_id)
        if habit:
            self.db.delete(habit)
            self.db.commit()
        return habit

    def update(self, habit_id: int, name: str = None, frequency=None) -> Habit | None:
        habit = self.get_by_id(habit_id)
        if habit:
            if name is not None:
                habit.name = name
            if frequency is not None:
                habit.frequency = frequency
            self.db.commit()
            self.db.refresh(habit)
        return habit

    # Metodos de leitura
    def get_by_name(self, name: str) -> Habit | None:
        return self.db.query(Habit).filter(Habit.name == name).first()
    
    def get_by_id(self, habit_id: int) -> Habit | None:
        return self.db.query(Habit).filter(Habit.id == habit_id).first()

    def get_all(self) -> list[Habit]:
        return self.db.query(Habit).all()


class RecordCRUD:
    def __init__(self, db: Session):
        self.db = db

    def create(self, habit_id: int) -> Record:
        record = Record(habit_id=habit_id)
        self.db.add(record)
        self.db.commit()
        self.db.refresh(record)
        return record

    def delete(self, record_id: int) -> Record | None:
        record = self.get_by_id(record_id)
        if record:
            self.db.delete(record)
            self.db.commit()
        return record


    # Metodos de leitura
    def get_by_habit_id(self, habit_id: int) -> list[Record]:
        return self.db.query(Record).filter(Record.habit_id == habit_id).all()
    
    def get_by_id(self, record_id: int) -> Record | None:
        return self.db.query(Record).filter(Record.id == record_id).first()

    def get_all(self) -> list[Record]:
        return self.db.query(Record).all()
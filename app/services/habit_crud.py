from sqlalchemy.orm import Session
from models.habit import Habit


class HabitCRUD:
    def __init__(self, db: Session):
        self.db = db

    def create(self, name: str, frequency=None) -> Habit:
        habit = Habit(name=name, frequency=frequency)
        self.db.add(habit)
        self.db.commit()
        self.db.refresh(habit)
        return habit

    def get_by_id(self, habit_id: int) -> Habit | None:
        return self.db.query(Habit).filter(Habit.id == habit_id).first()

    def get_all(self) -> list[Habit]:
        return self.db.query(Habit).all()

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

    def get_by_name(self, name: str) -> Habit | None:
        return self.db.query(Habit).filter(Habit.name == name).first()

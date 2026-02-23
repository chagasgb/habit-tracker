import datetime
from sqlalchemy.orm import Session

from services.crud import HabitCRUD, RecordCRUD


WEEKDAY_TO_ABBR = {
    0: "Mo",
    1: "Tu",
    2: "We",
    3: "Th",
    4: "Fr",
    5: "Sa",
    6: "Su",
}


class DaySummaryService:
    def __init__(self, db: Session):
        self.db = db
        self.habit_crud = HabitCRUD(db)
        self.record_crud = RecordCRUD(db)

    def get_day_summary(self, target_date: datetime.date):
        weekday_abbr = WEEKDAY_TO_ABBR[target_date.weekday()]

        # 1️⃣ hábitos agendados para o dia
        habits = self.habit_crud.get_all()
        scheduled_habits = [
            habit for habit in habits
            if habit.frequency and weekday_abbr in habit.frequency
        ]

        total_habits = len(scheduled_habits)

        # 2️⃣ registros do dia
        records = self.record_crud.get_all()
        records_today = [
            r for r in records
            if r.created_at.date() == target_date
        ]

        completed_habit_ids = {r.habit_id for r in records_today}
        completed_count = len(completed_habit_ids)

        percent = (
            int((completed_count / total_habits) * 100)
            if total_habits > 0
            else 0
        )

        return {
            "date": target_date.isoformat(),
            "total_habits": total_habits,
            "completed_count": completed_count,
            "percent": percent,
            "is_day_completed": total_habits > 0 and completed_count == total_habits,
            "habits": [
                {
                    "id": h.id,
                    "name": h.name,
                    "completed": h.id in completed_habit_ids,
                }
                for h in scheduled_habits
            ],
        }

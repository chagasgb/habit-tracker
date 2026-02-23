import datetime
from sqlalchemy.orm import Session
from services.day_summary_service import DaySummaryService


class CalendarService:
    def __init__(self, db: Session):
        self.db = db
        self.day_summary_service = DaySummaryService(db)

    def get_range(
        self, center: datetime.date, days_before: int = 0, days_after: int = 0
    ):
        """
        Retorna um range de dias com o dia central separado.

        - center: dia central do range (normalmente o dia atual)
        - days_before: quantos dias antes do center incluir
        - days_after: quantos dias depois do center incluir

        Payload separado:
        {
            "center": { ... },
            "days_before": [ ... ],
            "days_after": [ ... ]
        }
        """
        days_before_list = []
        days_after_list = []

        # dias antes do center
        for i in range(days_before, 0, -1):
            day = center - datetime.timedelta(days=i)
            summary = self.day_summary_service.get_day_summary(day)
            days_before_list.append({
                "date": day.isoformat(),
                "day": day.day,
                "weekday": day.strftime("%a"),
                "completed": summary["is_day_completed"],
                "percent": summary["percent"],
            })

        # dia central
        summary_center = self.day_summary_service.get_day_summary(center)
        center_day = {
            "date": center.isoformat(),
            "day": center.day,
            "weekday": center.strftime("%a"),
            "completed": summary_center["is_day_completed"],
            "percent": summary_center["percent"],
        }

        # dias depois do center
        for i in range(1, days_after + 1):
            day = center + datetime.timedelta(days=i)
            summary = self.day_summary_service.get_day_summary(day)
            days_after_list.append({
                "date": day.isoformat(),
                "day": day.day,
                "weekday": day.strftime("%a"),
                "completed": summary["is_day_completed"],
                "percent": summary["percent"],
            })

        return {
            "center": center_day,
            "days_before": days_before_list,
            "days_after": days_after_list,
        }

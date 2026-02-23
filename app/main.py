import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from core.database import Base, engine
from routes.records import router as record_router
from routes.habits import router as habit_router
from routes.day_summary import router as day_summary_router
from routes.calendar import router as calendar_router


# =========================
# DATABASE
# =========================
if not os.getenv("TESTING"):
    Base.metadata.create_all(bind=engine)


# =========================
# APP
# =========================
app = FastAPI(
    title="Habit Tracker API",
    version="0.1.0",
)


# =========================
# CORS (VUE / VITE)
# =========================
origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# =========================
# ROUTES
# =========================
app.include_router(habit_router, prefix="/habits", tags=["Habits"])
app.include_router(record_router, prefix="/records", tags=["Records"])
app.include_router(day_summary_router)
app.include_router(calendar_router)


# =========================
# HEALTH CHECK (opcional)
# =========================
@app.get("/health")
def health_check():
    return {"status": "ok"}

from fastapi import FastAPI
from models import Base
from database import engine

from routes.records import router as record_router  
from routes.habits import router as habit_router

# Criar as tabelas no PostgreSQL
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Habit Tracker API", version="0.1.0")

# Rotas da aplicação
app.include_router(habit_router, prefix="/habits", tags=["Habits"])
app.include_router(record_router, prefix="/records", tags=["Records"])
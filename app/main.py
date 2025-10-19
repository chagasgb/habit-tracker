from fastapi import FastAPI
from core.database import Base, engine


from routes.records import router as record_router  
from routes.habits import router as habit_router

# Apenas criar tabelas se não estivermos em modo de teste
import os
if not os.getenv("TESTING"):
    Base.metadata.create_all(bind=engine)

app = FastAPI(title="Habit Tracker API", 
              version="0.1.0")

@app.get("/health")
async def health_check():
    """Endpoint para verificação de saúde da aplicação"""
    return {"status": "healthy", "service": "habit-tracker"}

app.include_router(habit_router, prefix="/habits", tags=["Habits"])
app.include_router(record_router, prefix="/records", tags=["Records"])
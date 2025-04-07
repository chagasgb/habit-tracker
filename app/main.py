from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base
from routes import habit_router, record_router

# Configuração do banco de dados
DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Criar as tabelas
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Habit Tracker API", version="0.1.0")

# Configuração de templates
templates = Jinja2Templates(directory="templates")

# Configuração de arquivos estáticos
app.mount("/static", StaticFiles(directory="static"), name="static")

# Incluir rotas
app.include_router(habit_router, prefix="/habits", tags=["Habits"])
app.include_router(record_router, prefix="/records", tags=["Records"])

@app.get("/")
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)


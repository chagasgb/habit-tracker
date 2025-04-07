from fastapi import FastAPI, Request, Depends, HTTPException
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError

from models import Base
from database import engine, get_db
from routes import habit_router, record_router

# Criar as tabelas no PostgreSQL
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Habit Tracker API", version="0.1.0")

# Rotas da aplicação
app.include_router(habit_router, prefix="/habits", tags=["Habits"])
app.include_router(record_router, prefix="/records", tags=["Records"])

# Página de teste simples
@app.get("/", response_class=HTMLResponse)
async def read_root():
    html_content = """
    <!DOCTYPE html>
    <html>
        <head>
            <title>Hello</title>
        </head>
        <body>
            <h1>Hello, world!</h1>
            <p>FastAPI servindo HTML puro.</p>
        </body>
    </html>
    """
    return HTMLResponse(content=html_content)


# Endpoint de verificação do banco de dados
@app.get("/db-status")
def check_db_connection(db: Session = Depends(get_db)):
    try:
        result = db.execute(text("SELECT version();"))
        version = result.scalar()

        return {
            "status": "Conectado com sucesso ao banco de dados!",
            "postgres_version": version
        }

    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Erro na conexão com o banco: {str(e)}")

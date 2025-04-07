from fastapi import FastAPI, Request, Depends, HTTPException
from fastapi.responses import HTMLResponse


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
            <h1>Olá, Fast API</h1>
        </body>
    </html>
    """
    return HTMLResponse(content=html_content)

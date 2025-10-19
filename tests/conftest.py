import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import sys
import os

# Define variável de ambiente para modo de teste
os.environ["TESTING"] = "true"

# Adiciona o diretório app ao path para importar os módulos
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'app'))

from core.database import Base, get_db
from main import app

# Configurar banco de dados em memória para testes
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

@pytest.fixture
def client():
    """Fixture que fornece um cliente de teste para a aplicação FastAPI"""
    # Criar todas as tabelas antes dos testes
    Base.metadata.create_all(bind=engine)
    
    yield TestClient(app)
    
    # Limpar após os testes
    Base.metadata.drop_all(bind=engine)

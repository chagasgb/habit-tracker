# tests/test_records.py
import pytest
from fastapi.testclient import TestClient
from datetime import datetime, date


def test_create_record(client: TestClient):
    """Testa criação de registro de execução de hábito"""
    # Primeiro criar um hábito
    habit_data = {
        "name": "Exercitar-se",
        "frequency": ["Mo", "We", "Fr"]
    }
    habit_response = client.post("/habits", json=habit_data)
    habit_id = habit_response.json()["id"]
    
    # Criar registro de execução
    record_data = {
        "habit_id": habit_id
    }
    response = client.post("/records", json=record_data)
    
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert str(habit_id) in data["message"]


def test_get_all_records(client: TestClient):
    """Testa listagem de todos os registros"""
    # Criar alguns hábitos e registros
    habits_data = [
        {"name": "Hábito 1"},
        {"name": "Hábito 2"}
    ]
    
    habit_ids = []
    for habit_data in habits_data:
        habit_response = client.post("/habits", json=habit_data)
        habit_ids.append(habit_response.json()["id"])
    
    # Criar registros para cada hábito
    for habit_id in habit_ids:
        record_data = {"habit_id": habit_id}
        client.post("/records", json=record_data)
    
    # Buscar todos os registros
    response = client.get("/records")
    assert response.status_code == 200
    
    records = response.json()
    assert len(records) >= 2
    assert all("id" in record for record in records)
    assert all("habit_id" in record for record in records)
    assert all("timestamp" in record for record in records)


def test_get_records_by_habit(client: TestClient):
    """Testa busca de registros por hábito específico"""
    # Criar hábito
    habit_data = {"name": "Meditar"}
    habit_response = client.post("/habits", json=habit_data)
    habit_id = habit_response.json()["id"]
    
    # Criar alguns registros para o hábito (apenas 1 por dia devido à validação)
    record_data = {"habit_id": habit_id}
    client.post("/records", json=record_data)
    
    # Buscar registros do hábito específico
    response = client.get(f"/records?habit_id={habit_id}")
    assert response.status_code == 200
    
    records = response.json()
    assert len(records) == 1
    assert all(record["habit_id"] == habit_id for record in records)


def test_create_record_invalid_habit(client: TestClient):
    """Testa criação de registro com hábito inexistente"""
    record_data = {
        "habit_id": 99999  # ID que não existe
    }
    response = client.post("/records", json=record_data)
    
    assert response.status_code == 404


def test_create_record_invalid_data(client: TestClient):
    """Testa criação de registro com dados inválidos"""
    # Dados inválidos - falta habit_id
    record_data = {}
    response = client.post("/records", json=record_data)
    
    assert response.status_code == 422  # Validation error


def test_delete_record(client: TestClient):
    """Testa exclusão de registro"""
    # Criar hábito e registro
    habit_data = {"name": "Hábito para deletar"}
    habit_response = client.post("/habits", json=habit_data)
    habit_id = habit_response.json()["id"]
    
    record_data = {"habit_id": habit_id}
    record_response = client.post("/records", json=record_data)
    
    # Buscar o registro criado para obter o ID
    records_response = client.get(f"/records?habit_id={habit_id}")
    records = records_response.json()
    record_id = records[0]["id"]
    
    # Deletar o registro
    response = client.delete(f"/records/{record_id}")
    assert response.status_code == 200
    
    data = response.json()
    # Aceita tanto "detail" quanto "message"
    key = "detail" if "detail" in data else "message"
    assert key in data
    assert "deletado" in data[key].lower()


def test_delete_record_not_found(client: TestClient):
    """Testa exclusão de registro inexistente"""
    response = client.delete("/records/99999")
    assert response.status_code == 404

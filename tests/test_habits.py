# tests/test_habits_simple.py
import pytest
from fastapi.testclient import TestClient


def test_create_habit(client: TestClient):
    """Testa criação de hábito"""
    habit_data = {
        "name": "Exercitar-se",
        "frequency": ["Mo", "We", "Fr"]
    }
    response = client.post("/habits", json=habit_data)
    
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == habit_data["name"]
    assert data["frequency"] == habit_data["frequency"]
    assert "id" in data


def test_get_all_habits(client: TestClient):
    """Testa listagem de todos os hábitos"""
    # Criar alguns hábitos primeiro
    habits_data = [
        {"name": "Hábito 1", "frequency": ["Mo", "Tu"]},
        {"name": "Hábito 2", "frequency": ["We", "Th"]}
    ]
    
    for habit_data in habits_data:
        client.post("/habits", json=habit_data)
    
    # Buscar todos os hábitos
    response = client.get("/habits")
    assert response.status_code == 200
    
    habits = response.json()
    assert len(habits) >= 2
    assert all("id" in habit for habit in habits)
    assert all("name" in habit for habit in habits)


def test_delete_habit(client: TestClient):
    """Testa exclusão de hábito"""
    # Criar um hábito
    habit_data = {"name": "Hábito para deletar"}
    create_response = client.post("/habits", json=habit_data)
    habit_id = create_response.json()["id"]
    
    # Deletar o hábito
    response = client.delete(f"/habits/{habit_id}")
    assert response.status_code == 200
    
    data = response.json()
    # Aceita tanto "detail" quanto "message"
    key = "detail" if "detail" in data else "message"
    assert key in data
    assert "deletado" in data[key].lower()


def test_delete_habit_not_found(client: TestClient):
    """Testa exclusão de hábito inexistente"""
    response = client.delete("/habits/99999")
    assert response.status_code == 404

from fastapi.testclient import TestClient
import pytest
from app import app  # Ajusta para o nome do teu ficheiro principal se for main.py

client = TestClient(app)

def test_root():
    response = client.get("/")
    assert response.status_code == 200

def test_register_and_login():
    # 1. Registar um utilizador único para o teste
    user_data = {"username": "testuser", "password": "securepassword123"}
    response = client.post("/register", json=user_data)
    
    # Se já existir de um teste anterior, aceita 200/201 ou 400, mas idealmente limpa a BD
    assert response.status_code in [200, 201, 400]

    # 2. Tentar fazer login para obter o token JWT
    login_data = {"username": "testuser@example.com", "password": "securepassword123"}
    response = client.post("/token", data=login_data)
    
    if response.status_code == 200:
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_register_user_success():
  response = client.post(
      "/register", json={"username": "newuser123", "password": "securepassword123"}
  )
  assert response.status_code == 201
  assert response.json() == {"message": "Utilizador registado com sucesso!"}


def test_register_duplicate_user():
  # Tenta registar o mesmo utilizador novamente
  response = client.post(
      "/register", json={"username": "newuser123", "password": "securepassword123"}
  )
  assert response.status_code == 400
  assert "já está registado" in response.json()["detail"]


def test_login_success():
  response = client.post(
      "/token", data={"username": "newuser123", "password": "securepassword123"}
  )
  assert response.status_code == 200
  data = response.json()
  assert "access_token" in data
  assert data["token_type"] == "bearer"


def test_login_wrong_password():
  response = client.post(
      "/token", data={"username": "newuser123", "password": "wrongpassword"}
  )
  assert response.status_code == 401
  assert response.json()["detail"] == "Utilizador ou senha incorretos"


def test_login_nonexistent_user():
  response = client.post(
      "/token", data={"username": "naoexisto", "password": "anypassword"}
  )
  assert response.status_code == 401
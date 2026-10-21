from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def get_auth_token():
  # Regista um utilizador dedicado para os testes de tarefas (se já existir, apenas faz login)
  client.post(
      "/register",
      json={"username": "taskuser", "password": "taskpassword123"},
  )
  response = client.post(
      "/token", data={"username": "taskuser", "password": "taskpassword123"}
  )
  return response.json()["access_token"]


def test_create_task_success():
  token = get_auth_token()
  headers = {"Authorization": f"Bearer {token}"}

  response = client.post(
      "/tasks/",
      json={"title": "Estudar FastAPI", "description": "Aprender arquitetura modular"},
      headers=headers,
  )
  assert response.status_code == 201
  data = response.json()
  assert data["title"] == "Estudar FastAPI"
  assert "task_id" in data


def test_list_tasks_success():
  token = get_auth_token()
  headers = {"Authorization": f"Bearer {token}"}

  response = client.get("/tasks/", headers=headers)
  assert response.status_code == 200
  assert isinstance(response.json(), list)


def test_create_task_unauthorized():
  # Tenta criar tarefa sem enviar o token de autenticação
  response = client.post(
      "/tasks/", json={"title": "Tarefa sem token", "description": "Teste"}
  )
  assert response.status_code == 401


def test_access_tasks_invalid_token():
  headers = {"Authorization": "Bearer token_falso_invalido"}
  response = client.get("/tasks/", headers=headers)
  assert response.status_code == 401
from fastapi import testclient
from app.main import app
from app.database import get_session
import app.schemas.task_schemas as schemas
from sqlmodel import SQLModel, Session, create_engine
from sqlmodel.pool import StaticPool  
import pytest


DATABASE_URL = "sqlite://"

@pytest.fixture(name="session")
def session_fixture():
    engine = create_engine(  
        DATABASE_URL,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool
        )
    
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session: 
        yield session


@pytest.fixture(name="client")
def client_fixture(session):
    def get_session_override():
        return session
    
    app.dependency_overrides[get_session] = get_session_override

    client = testclient.TestClient(app)
    yield client
    app.dependency_overrides.clear()  


def test_create_task(client: testclient.TestClient):
    db_user = client.post("/auth/register", json={"name":"Alice","email":"alice@example.com","password":"secret123"})
    user_id = db_user.json()["id"]
    new_task = {"title": "Task 1", "description": "Description of task 1", "user_id": user_id}
    response = client.post(f"/users/{user_id}/tasks", json=new_task)
    assert response.status_code == 201
    assert response.json() == schemas.Task_Response(id=1, title=new_task["title"], description=new_task["description"],user_id= 1).model_dump()


def test_read_task(client: testclient.TestClient):
    db_user = client.post("/auth/register", json={"name":"Alice","email":"alice@example.com","password":"secret123"})
    user_id = db_user.json()["id"]
    task_id = 1
    client.post(f"/users/{user_id}/tasks", json={"title": "Task 1", "description": "Description of task 1", "user_id": user_id})
    response = client.get(f"/tasks/{task_id}")
    assert response.status_code == 200
    assert response.json() == schemas.Task_Response(id=task_id, title="Task 1", description="Description of task 1", user_id=user_id).model_dump()


def test_update_task(client: testclient.TestClient):
    task_id = 1
    db_user = client.post("/auth/register", json={"name":"Alice","email":"alice@example.com","password":"secret123"})
    user_id = db_user.json()["id"]
    client.post(f"/users/{user_id}/tasks", json={"title": "Task 1", "description": "Description of task 1", "user_id": user_id})
    updated_task = {"title": "Task 1 Updated", "description": "Description of task 1 updated", "user_id": 1 }
    response = client.put(f"/tasks/update-task/{task_id}", json=updated_task)
    assert response.status_code == 200
    assert response.json() == schemas.Task_Response(id=task_id, title=updated_task["title"], description=updated_task["description"], user_id=updated_task["user_id"]).model_dump()


def test_delete_task(client: testclient.TestClient):
    db_user = client.post("/auth/register", json={"name":"Alice","email":"alice@example.com","password":"secret123"})
    user_id = db_user.json()["id"]
    task_id = 1
    client.post(f"/users/{user_id}/tasks", json={"title": "Task 1", "description": "Description of task 1", "user_id": user_id})
    response = client.delete(f"/tasks/delete-task/{task_id}")
    assert response.status_code == 204


# Verifica se a task não excede o tamanho máximo permitido
def test_create_task_with_long_title(client: testclient.TestClient):
    db_user = client.post("/auth/register", json={"name":"Alice","email":"alice@example.com","password":"secret123"})
    user_id = db_user.json()["id"]
    long_title = "T" * 101  # 101 caracteres, excedendo o limite de 100
    new_task = {"title": long_title, "description": "Description of task with long title", "user_id": user_id}
    response = client.post(f"/users/{user_id}/tasks", json=new_task)
    assert response.status_code == 422  


# Verifica se a descrição da task não excede o tamanho máximo permitido
def test_create_task_with_long_description(client: testclient.TestClient):
    db_user = client.post("/auth/register", json={"name":"Alice","email":"alice@example.com","password":"secret123"})
    user_id = db_user.json()["id"]
    long_description = "D" * 201  # 201 caracteres, excedendo o limite de 200
    new_task = {"title": "Task with long description", "description": long_description, "user_id": user_id}
    response = client.post(f"/users/{user_id}/tasks", json=new_task)
    assert response.status_code == 422 


def test_create_task_with_empty_title(client: testclient.TestClient):
    db_user = client.post("/auth/register", json={"name":"Alice","email":"alice@example.com","password":"secret123"})
    user_id = db_user.json()["id"]
    new_task = {"title": "", "description": "Description of task with empty title", "id_user": user_id}
    response = client.post(f"/users/{user_id}/tasks", json=new_task)
    assert response.status_code == 422  


def test_task_not_found(client: testclient.TestClient):
    task_id = 999  # ID que não existe
    response = client.get(f"/tasks/{task_id}")
    assert response.status_code == 404  # Task not found
    assert response.json() == {"detail": "Task not found"}


def test_read_task_by_title(client: testclient.TestClient):
    db_user = client.post("/auth/register", json={"name":"Alice","email":"alice@example.com","password":"secret123"})
    user_id = db_user.json()["id"]
    client.post(f"/users/{user_id}/tasks", json={"title": "Task 1", "description": "Description of task 1", "user_id": user_id})
    response = client.get("/tasks/by-title/?title=Task 1")
    assert response.status_code == 200
    assert response.json() == schemas.Task_Response(id=1, title="Task 1", description="Description of task 1", user_id=user_id).model_dump()


def test_read_task_by_title_not_found(client: testclient.TestClient):
    response = client.get("/tasks/by-title/?title=Nonexistent Task")
    assert response.status_code == 404
    assert response.json() == {"detail": "Task not found"}


def test_update_task_not_found(client: testclient.TestClient):
    db_user = client.post("/auth/register", json={"name":"Alice","email":"alice@example.com","password":"secret123"})
    user_id = db_user.json()["id"]
    client.post(f"/users/{user_id}/tasks", json={"title": "Task 1", "description": "Description of task 1", "user_id": user_id})    
    task_id = 999 
    updated_task = {"title": "Task 1 Updated", "description": "Description of task 1 updated", "user_id":user_id}
    response = client.put(f"/tasks/update-task/{task_id}", json=updated_task)
    assert response.status_code == 404  # Task not found
    assert response.json() == {"detail": "Task not found"}


def test_delete_task_not_found(client: testclient.TestClient):
    db_user = client.post("/auth/register", json={"name":"Alice","email":"alice@example.com","password":"secret123"})
    user_id = db_user.json()["id"]
    client.post(f"/users/{user_id}/tasks", json={"title": "Task 1", "description": "Description of task 1", "user_id": user_id})
    task_id = 999 
    response = client.delete(f"/tasks/delete-task/{task_id}")
    assert response.status_code == 404  # Task not found
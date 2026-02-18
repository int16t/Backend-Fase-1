from fastapi import testclient
from app.main import app
from app.routers.tasks import Task_response
from app.database import get_session
from app.models.model_tasks import Task  # Importar para registrar no metadata
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
    new_task = {"title": "Task 1", "description": "Description of task 1"}
    response = client.post("/tasks/create-task", json=new_task)
    assert response.status_code == 201
    assert response.json() == Task_response(title=new_task["title"], description=new_task["description"]).model_dump()


def test_read_tasks(client: testclient.TestClient):
    # Criar task primeiro
    client.post("/tasks/create-task", json={"title": "Task 1", "description": "Description of task 1"})
    
    response = client.get("/tasks/")
    tasks = response.json()
    assert response.status_code == 200
    assert len(tasks) >= 1
    assert any(t["title"] == "Task 1" and t["description"] == "Description of task 1" for t in tasks)


def test_read_task(client: testclient.TestClient):
    # Criar task primeiro
    client.post("/tasks/create-task", json={"title": "Task 1", "description": "Description of task 1"})
    
    task_id = 1
    response = client.get(f"/tasks/{task_id}")
    assert response.status_code == 200
    assert response.json() == {"id": task_id, "title": "Task 1", "description": "Description of task 1"}


def test_update_task(client: testclient.TestClient):
    # Criar task primeiro
    client.post("/tasks/create-task", json={"title": "Task 1", "description": "Description of task 1"})
    
    task_id = 1
    updated_task = {"title": "Task 1 Updated", "description": "Description of task 1 updated"}
    response = client.put(f"/tasks/update-task/{task_id}", json=updated_task)
    assert response.status_code == 200
    assert response.json() == Task_response(title=updated_task["title"], description=updated_task["description"]).model_dump()


def test_delete_task(client: testclient.TestClient):
    # Criar task primeiro
    client.post("/tasks/create-task", json={"title": "Task 1", "description": "Description of task 1"})
    
    task_id = 1
    response = client.delete(f"/tasks/delete-task/{task_id}")
    assert response.status_code == 204
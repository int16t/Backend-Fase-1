from fastapi import testclient
from app.main import app
from app.database import get_session
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


def test_read_tasks(client: testclient.TestClient):
    db_user = client.post("users/create-user", json={"name":"Alice","email":"alice@example.com"})
    user_id = db_user.json()["id"]

    client.post(f"/admin/users/{user_id}/task", json={"title": "Task 1", "description": "Description of task 1", "user_id": user_id})
    client.post(f"/admin/users/{user_id}/task", json={"title": "Task 2", "description": "Description of task 2", "user_id": user_id})
    client.post(f"/admin/users/{user_id}/task", json={"title": "Task 3", "description": "Description of task 3", "user_id": user_id})

    response = client.get("/admin/tasks")
    tasks = response.json()
    assert response.status_code == 200
    assert len(tasks) >= 1
    assert any(t["title"] == "Task 1" and t["description"] == "Description of task 1" and t["user_id"] == 1 for t in tasks)


def test_read_users(client: testclient.TestClient):
    client.post("users/create-user", json={"name":"Alice","email":"alice@example.com"})
    client.post("users/create-user", json={"name":"Breno","email":"breno@example.com"})
    response = client.get("/admin/users")
    assert response.status_code == 200
    users = response.json()
    assert len(users) >= 1
    # Verifica se o usuário criado existe
    assert any(u["name"] == "Alice" and u["email"] == "alice@example.com" for u in users)
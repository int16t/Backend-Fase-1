from fastapi import testclient
from app.main import app
from app.models.model_users import User  # Importar para registrar no metadata
from app.routers.users import User_response
from app.database import get_session
from sqlmodel import SQLModel, Session, StaticPool, create_engine
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


def test_create_user(client: testclient.TestClient):
    new_user = {"name": "Alice", "email": "alice@example.com"}
    response = client.post("/users/create-user", json=new_user)
    assert response.status_code == 201
    assert response.json() == User_response(name=new_user["name"], email=new_user["email"]).model_dump()


def test_read_user(client: testclient.TestClient):
    client.post("/users/create-user", json={"name": "Alice", "email": "alice@example.com"})
    user_id = 1
    response = client.get(f"/users/{user_id}")
    assert response.status_code == 200
    assert response.json() == {"id": user_id, "name": "Alice", "email": "alice@example.com"}


def test_read_users(client: testclient.TestClient):
    client.post("/users/create-user", json={"name": "Alice", "email": "alice@example.com"})
    response = client.get("/users/")
    assert response.status_code == 200
    users = response.json()
    assert len(users) >= 1
    # Verifica se o usuário criado existe
    assert any(u["name"] == "Alice" and u["email"] == "alice@example.com" for u in users)


def test_update_user(client: testclient.TestClient):
    client.post("/users/create-user", json={"name": "Alice", "email": "alice@example.com"})
    user_id = 1
    updated_user = {"name": "Alice Updated", "email": "alice.updated@example.com"}
    response = client.put(f"/users/update-user/{user_id}", json=updated_user)
    assert response.status_code == 200
    assert response.json() == User_response(name=updated_user["name"], email=updated_user["email"]).model_dump()


def test_delete_user(client: testclient.TestClient):
    client.post("/users/create-user", json={"name": "Alice", "email": "alice@example.com"}) 
    user_id = 1
    response = client.delete(f"/users/delete-user/{user_id}")
    assert response.status_code == 204


def test_create_user_with_long_name(client: testclient.TestClient):
    long_name = "N" * 101  # 101 caracteres, excedendo o limite de 100
    new_user = {"name": long_name, "email": "alice@example.com"}
    response = client.post("/users/create-user", json=new_user)
    assert response.status_code == 422  # Unprocessable Entity


def test_create_user_with_long_email(client: testclient.TestClient):
    long_email = "E" * 18 + "@example.com.br"  # Excedendo o limite de 30 caracteres para o email
    new_user = {"name": "Alice", "email": long_email}
    response = client.post("/users/create-user", json=new_user)
    assert response.status_code == 422  # Unprocessable Entity
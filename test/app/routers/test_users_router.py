from fastapi import testclient
from app.main import app
from app.schemas.user_schemas import User_Response  # Importar para registrar no metadata
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
    new_user = {"name": "Alice", "email": "alice@example.com", "password": "secret123"}
    response = client.post("/auth/register", json=new_user)
    assert response.status_code == 201
    assert response.json() == User_Response(id=1, name=new_user["name"], email=new_user["email"]).model_dump()


def test_read_user(client: testclient.TestClient):
    client.post("/auth/register", json={"name": "Alice", "email": "alice@example.com", "password": "secret123"})
    login = client.post("/auth/login", data={"username": "alice@example.com", "password": "secret123"})
    headers = {"Authorization": f"Bearer {login.json()['access_token']}"}
    user_id = 1
    response = client.get(f"/users/{user_id}", headers=headers)
    assert response.status_code == 200
    assert response.json() == User_Response(id=user_id, name="Alice", email="alice@example.com").model_dump()


def test_read_user_by_email(client: testclient.TestClient):
    client.post("/auth/register", json={"name": "Alice", "email": "alice@example.com", "password": "secret123"})
    login = client.post("/auth/login", data={"username": "alice@example.com", "password": "secret123"})
    headers = {"Authorization": f"Bearer {login.json()['access_token']}"}
    response = client.get("/users/by-email/?email=alice@example.com", headers=headers)
    assert response.status_code == 200
    assert response.json() == User_Response(id=1, name="Alice", email="alice@example.com").model_dump()


def test_update_user(client: testclient.TestClient):
    client.post("/auth/register", json={"name": "Alice", "email": "alice@example.com", "password": "secret123"})
    login = client.post("/auth/login", data={"username": "alice@example.com", "password": "secret123"})
    token = login.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    user_id = 1
    updated_user = {"name": "Alice Updated", "email": "alice.updated@example.com", "password":"secret123"}
    response = client.put(f"/users/update-user/{user_id}", json=updated_user, headers=headers)
    assert response.status_code == 200
    assert response.json() == User_Response(id=user_id, name=updated_user["name"], email=updated_user["email"]).model_dump()


def test_delete_user(client: testclient.TestClient):
    client.post("/auth/register", json={"name": "Alice", "email": "alice@example.com", "password": "secret123"})
    login = client.post("/auth/login", data={"username": "alice@example.com", "password": "secret123"})
    token = login.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    user_id = 1
    response = client.delete(f"/users/delete-user/{user_id}", headers=headers)
    assert response.status_code == 204


def test_create_user_with_long_name(client: testclient.TestClient):
    long_name = "N" * 101  # 101 caracteres, excedendo o limite de 100
    new_user = {"name": long_name, "email": "alice@example.com", "password": "secret123"}
    response = client.post("/auth/register", json=new_user)
    assert response.status_code == 422  # Unprocessable Entity


def test_create_user_with_long_email(client: testclient.TestClient):
    long_email = "E" * 18 + "@example.com.br"  # Excedendo o limite de 30 caracteres para o email
    new_user = {"name": "Alice", "email": long_email, "password": "secret123"}
    response = client.post("/auth/register", json=new_user)
    assert response.status_code == 422  # Unprocessable Entity


def test_create_user_with_invalid_email(client: testclient.TestClient):
    invalid_email = "invalid-email"  # Email sem formato válido
    new_user = {"name": "Alice", "email": invalid_email, "password": "secret123"}
    response = client.post("/auth/register", json=new_user)
    assert response.status_code == 422  # Unprocessable Entity


def test_user_not_found(client: testclient.TestClient):
    client.post("/auth/register", json={"name": "Alice", "email": "alice@example.com", "password": "secret123"})
    login = client.post("/auth/login", data={"username": "alice@example.com", "password": "secret123"})
    headers = {"Authorization": f"Bearer {login.json()['access_token']}"}
    user_id = 999  # ID que não existe nem pertence ao usuário
    response = client.get(f"/users/{user_id}", headers=headers)
    assert response.status_code == 403  # ownership check falha antes de buscar no banco


def test_read_user_by_email_not_found(client: testclient.TestClient):
    client.post("/auth/register", json={"name": "Alice", "email": "alice@example.com", "password": "secret123"})
    login = client.post("/auth/login", data={"username": "alice@example.com", "password": "secret123"})
    headers = {"Authorization": f"Bearer {login.json()['access_token']}"}
    response = client.get("/users/by-email/?email=test@example.com", headers=headers)
    assert response.status_code == 403  # email não pertence ao usuário autenticado


def test_update_user_not_found(client: testclient.TestClient):
    client.post("/auth/register", json={"name": "Alice", "email": "alice@example.com", "password": "secret123"})
    login = client.post("/auth/login", data={"username": "alice@example.com", "password": "secret123"})
    token = login.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    user_id = 999 
    updated_user = {"name": "Alice Updated", "email": "alice.updated@example.com", "password": "secret123"}
    response = client.put(f"/users/update-user/{user_id}", json=updated_user, headers=headers)
    assert response.status_code == 403

def test_delete_user_not_found(client: testclient.TestClient):
    client.post("/auth/register", json={"name": "Alice", "email": "alice@example.com", "password": "secret123"})
    login = client.post("/auth/login", data={"username": "alice@example.com", "password": "secret123"})
    token = login.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    user_id = 999 
    response = client.delete(f"/users/delete-user/{user_id}", headers=headers)
    assert response.status_code == 403
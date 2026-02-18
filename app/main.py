from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.routers import tasks, users
# from app.database import create_db_and_tables
from app.models import *  # Importa os modelos para registrar no SQLModel.metadata
import uvicorn


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Código que roda na inicialização
    # create_db_and_tables()
    yield
    # Código que roda no encerramento (opcional)


app = FastAPI(lifespan=lifespan)


@app.get("/")
async def root_directory() -> str:
    return "Hello, World!"


app.include_router(tasks.router)
app.include_router(users.router)


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
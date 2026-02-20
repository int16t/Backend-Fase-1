from contextlib import asynccontextmanager
from app.exceptions import EmailAlreadyExistsError, NotFound, NotAllowed
from fastapi import FastAPI, Request
from app.routers import tasks, users, admin, auth
from app.models import *  # Importa os modelos para registrar no SQLModel.metadata
from fastapi.responses import JSONResponse
import uvicorn


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Código que roda na inicialização
    yield
    # Código que roda no encerramento (opcional)


app = FastAPI(lifespan=lifespan)


@app.get("/")
async def root_directory() -> str:
    return "Hello, World!"


@app.exception_handler(NotFound)
async def not_found_handler(request: Request, exc: NotFound):
    return JSONResponse(status_code=404, content={"detail": f"{exc.name} not found"})

@app.exception_handler(EmailAlreadyExistsError)
async def email_exists_handler(request: Request, exc: EmailAlreadyExistsError):
    return JSONResponse(status_code=409, content={"detail": f"Email {exc.email} already exists"})

@app.exception_handler(NotAllowed)
async def email_exists_handler(request: Request, exc: NotAllowed):
    return JSONResponse(status_code=401, content={"detail": f"Page {exc.name} not Allowed!"})

app.include_router(tasks.router)
app.include_router(users.router)
app.include_router(admin.router)
app.include_router(auth.router)

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
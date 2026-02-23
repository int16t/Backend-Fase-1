from typing import Annotated
from fastapi import Depends
from sqlmodel import Session, SQLModel, create_engine
from app.config import DATABASE_URL

# Configurações do banco de dados PostgreSQL


engine = create_engine(DATABASE_URL)

# Cria a sessão de banco de dados
def get_session():
    with Session(engine) as session:
        yield session

SessionDep = Annotated[Session, Depends(get_session)]
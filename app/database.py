from typing import Annotated
from fastapi import Depends
from sqlmodel import Session, SQLModel, create_engine

# Configurações do banco de dados PostgreSQL
DATABASE_URL = "postgresql://admin:admin123@localhost:5432/meubanco"

engine = create_engine(DATABASE_URL)

# Cria as tabelas
# def create_db_and_tables():
#     SQLModel.metadata.drop_all(engine)  # Remove as tabelas existentes (opcional, para testes)
#     SQLModel.metadata.create_all(engine)

# Cria a sessão de banco de dados
def get_session():
    with Session(engine) as session:
        yield session

SessionDep = Annotated[Session, Depends(get_session)]
from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel
from app.database import SessionDep
from typing_extensions import Annotated
from sqlmodel import Field, select
from app.models.model_users import User
import app.crud.crud_users as crud


router = APIRouter(
    prefix="/users",
    tags=["users"],
)

class User_base(BaseModel):
    id: int
    name: str = Field(min_length=1, max_length=100)
    email: str = Field(min_length=1, max_length=30)


class User_response(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    email: str = Field(min_length=1, max_length=30)


@router.get("/")
async def read_users(
    session: SessionDep,
    offset: int = 0,
    limit: Annotated[int, Query(le=100)] = 100
    ):
    users = crud.get_users(session, offset, limit)
    return users


@router.get("/{user_id}")
async def read_user(user_id: int, session: SessionDep):
    user = crud.get_user_by_id(session, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.get("/by-email/")
async def read_user_by_email(email: str, session: SessionDep):
    user = crud.get_user_by_email(session, email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.post("/create-user", status_code=201)
async def create_user(user: User_response, session: SessionDep):
    db_user = crud.create_user(session, name=user.name, email=user.email)
    return db_user if db_user else HTTPException(status_code=400, detail="User could not be created")


@router.put("/update-user/{user_id}", status_code=200)
async def update_user(user_id: int, user: User_response, session: SessionDep):
    db_user = crud.update_user(session, user_id=user_id, name=user.name, email=user.email)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@router.delete("/delete-user/{user_id}", status_code=204)
async def delete_user(user_id: int, session: SessionDep):
    user = crud.delete_user(session, user_id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    pass
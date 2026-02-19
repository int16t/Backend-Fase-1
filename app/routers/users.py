from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel
from app.database import SessionDep
from typing_extensions import Annotated
from sqlmodel import Field, select
from app.models.model_users import User


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
    ) -> list[User_base]:
    users = session.exec(select(User).offset(offset).limit(limit)).all()
    return [User_base(id=user.id, name=user.name, email=user.email) for user in users]


@router.get("/{user_id}")
async def read_user(user_id: int, session: SessionDep):
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.post("/create-user", status_code=201)
async def create_user(user: User_response, session: SessionDep):
    db_user = User(name=user.name, email=user.email)
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return User_response(name=db_user.name, email=db_user.email)


@router.put("/update-user/{user_id}", status_code=200)
async def update_user(user_id: int, user: User_response, session: SessionDep):
    db_user = session.get(User, user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    db_user.name = user.name
    db_user.email = user.email
    session.commit()
    session.refresh(db_user)
    return User_response(name=db_user.name, email=db_user.email)


@router.delete("/delete-user/{user_id}", status_code=204)
async def delete_user(user_id: int, session: SessionDep):
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    session.delete(user)
    session.commit()
    pass
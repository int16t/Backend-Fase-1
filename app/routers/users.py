from fastapi import APIRouter, HTTPException, Query
from app.database import SessionDep
from typing_extensions import Annotated
import app.schemas.user_schemas as schemas
import app.crud.crud_users as crud

router = APIRouter(
    prefix="/users",
    tags=["users"],
)


@router.get("/")
async def read_users(
    session: SessionDep,
    offset: int = 0,
    limit: Annotated[int, Query(le=100)] = 100
    ):
    users = crud.get_users(session, offset, limit)
    if not users:
        raise HTTPException(status_code=404, detail="No users found")
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
async def create_user(user: schemas.User_Create, session: SessionDep):
    db_user = crud.create_user(session, name=user.name, email=user.email)
    if not db_user:
        raise HTTPException(status_code=400, detail="User could not be created")
    return db_user


@router.put("/update-user/{user_id}", status_code=200)
async def update_user(user_id: int, user: schemas.User_Update, session: SessionDep):
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
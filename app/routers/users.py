from fastapi import APIRouter
from app.database import SessionDep
from typing_extensions import Annotated
import app.schemas.user_schemas as schemas
import app.crud.crud_users as crud

router = APIRouter(
    prefix="/users",
    tags=["users"],
)

@router.get("/")
async def read_users(session: SessionDep):
    return crud.get_users(session)


@router.get("/{user_id}")
async def read_user(user_id: int, session: SessionDep):
    return crud.get_user_by_id(session, user_id=user_id)


@router.get("/by-email/")
async def read_user_by_email(email: str, session: SessionDep):
    return crud.get_user_by_email(session, email=email)


@router.post("/create-user", status_code=201)
async def create_user(user: schemas.User_Create, session: SessionDep):
    return crud.create_user(session, name=user.name, email=user.email)


@router.put("/update-user/{user_id}", status_code=200)
async def update_user(user_id: int, user: schemas.User_Update, session: SessionDep):
    return crud.update_user(session, user_id=user_id, name=user.name, email=user.email)


@router.delete("/delete-user/{user_id}", status_code=204)
async def delete_user(user_id: int, session: SessionDep):
    return crud.delete_user(session, user_id=user_id)
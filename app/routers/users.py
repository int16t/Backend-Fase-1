from fastapi import APIRouter
from app.database import SessionDep
import app.schemas.user_schemas as schemas_user
import app.schemas.task_schemas as schemas_task
import app.crud.crud_users as crud_users
import app.crud.crud_tasks as crud_tasks

router = APIRouter(
    prefix="/users",
    tags=["users"],
)

@router.get("/{user_id}/tasks", status_code=200)
async def get_tasks_for_user(session: SessionDep, user_id: int):
    return crud_tasks.get_tasks_user(session, user_id)


@router.get("/{user_id}", response_model=schemas_user.User_Response)
async def read_user(user_id: int, session: SessionDep):
    return crud_users.get_user_by_id(session, user_id=user_id)


@router.get("/by-email/", response_model=schemas_user.User_Response)
async def read_user_by_email(email: str, session: SessionDep):
    return crud_users.get_user_by_email(session, email=email)


@router.post("/{user_id}/tasks", status_code=201)
async def create_task_for_user(task: schemas_task.Task_Create, session: SessionDep):
    return crud_tasks.create_task(session, title=task.title, description=task.description, user_id=task.user_id)


@router.put("/update-user/{user_id}", status_code=200, response_model=schemas_user.User_Response)
async def update_user(user_id: int, user: schemas_user.User_Update, session: SessionDep):
    return crud_users.update_user(session, user_id=user_id, name=user.name, email=user.email)


@router.delete("/delete-user/{user_id}", status_code=204)
async def delete_user(user_id: int, session: SessionDep):
    return crud_users.delete_user(session, user_id=user_id)
from fastapi import APIRouter
from app.database import SessionDep, Depends
import app.crud.crud_users as crud_users
import app.crud.crud_tasks as crud_tasks
import app.schemas.task_schemas as schemas_task
import app.schemas.user_schemas as schemas_user
from app.dependencies import auth


router = APIRouter(
    prefix="/admin",
    tags=["admin"],
    dependencies=[Depends(auth.require_admin)]
)

@router.get("/users")
async def read_all_users(session: SessionDep):
    return crud_users.get_users(session)


@router.get("/tasks")
async def read_all_tasks(session: SessionDep):
    return crud_tasks.get_tasks(session)


@router.post("/create-user", status_code=201)
async def create_user(user: schemas_user.User_Create, session: SessionDep):
    return crud_users.create_user(session, name=user.name, email=user.email, password=user)


@router.post("/users/{user_id}/task")
async def create_task_for_admin(task: schemas_task.Task_Create, session: SessionDep):
    return crud_tasks.create_task(session, title=task.title, description=task.description, user_id=task.user_id)


@router.delete("/users/{user_id}", status_code=204)
async def delete_user(user_id: int, session: SessionDep):
    return crud_users.delete_user(session, user_id=user_id)
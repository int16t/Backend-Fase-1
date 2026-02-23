from fastapi import APIRouter, Query
from app.database import SessionDep, Depends
from app.services import user_services, task_services
import app.schemas.task_schemas as schemas_task
import app.schemas.user_schemas as schemas_user
from app.dependencies import auth
from typing import List

router = APIRouter(
    prefix="/admin",
    tags=["admin"],
    dependencies=[Depends(auth.require_admin)]
)

@router.get("/users", response_model=List[schemas_user.User_Response])
async def read_all_users(
    session: SessionDep,
    offset: int = Query(default=0, ge=0),
    limit: int = Query(default=10, ge=1, le=100)):
    return user_services.get_all(session, offset, limit)


@router.get("/tasks", response_model=List[schemas_task.Task_Response])
async def read_all_tasks(
    session: SessionDep,
    offset: int = Query(default=0, ge=0),
    limit: int = Query(default=10, ge=1, le=100)  # máximo 100 por página
):
    return task_services.get_all(session, offset, limit)


@router.post("/create-user", status_code=201)
async def create_user(user: schemas_user.User_Create, session: SessionDep):
    return user_services.create(session, name=user.name, email=user.email, password=user.password)


@router.post("/users/{user_id}/task")
async def create_task_for_admin(task: schemas_task.Task_Create, session: SessionDep):
    return task_services.create_admin(session, title=task.title, description=task.description, user_id=task.user_id)


@router.put("/update-user/{user_id}", status_code=200, response_model=schemas_user.User_Response)
async def update_user(user_id: int, user: schemas_user.User_Update, session: SessionDep):
    return user_services.update_admin(session, user_id=user_id, name=user.name, email=user.email, password=user.password)


@router.put("/update-task/{task_id}", status_code=200)
async def update_task(task_id: int, task: schemas_task.Task_Update, session: SessionDep):
    return task_services.update_admin(session, task_id=task_id, title=task.title, description=task.description)


@router.delete("/users/{user_id}", status_code=204)
async def delete_user(user_id: int, session: SessionDep):
    return user_services.delete(session, user_id=user_id)


@router.delete("/delete-task/{task_id}", status_code=204)
async def delete_task(session: SessionDep, task_id: int):
    return task_services.delete_admin(session, task_id=task_id)
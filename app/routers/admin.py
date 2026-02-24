from fastapi import APIRouter, Query
from app.database import SessionDep, Depends
import app.schemas.task_schemas as schemas_task
import app.schemas.user_schemas as schemas_user
from app.dependencies import auth
from typing import List, Annotated
from app.services.user_services import UserService
from app.services.task_services import TaskService
from app.repositories.user_repository import UserRepository
from app.repositories.task_repository import TaskRepository


router = APIRouter(
    prefix="/admin",
    tags=["admin"],
    dependencies=[Depends(auth.require_admin)]
)


def get_user_service(session: SessionDep) -> UserService:
    return UserService(UserRepository(session))

def get_task_service(session: SessionDep) -> TaskService:
    return TaskService(TaskRepository(session))

UserServiceDep = Annotated[UserService, Depends(get_user_service)]
TaskServiceDep = Annotated[TaskService, Depends(get_task_service)]


@router.get("/users", response_model=List[schemas_user.User_Response])
async def read_all_users(
    service: UserServiceDep,
    offset: int = Query(default=0, ge=0),
    limit: int = Query(default=10, ge=1, le=100)):
    return service.get_all(offset, limit)


@router.get("/tasks", response_model=List[schemas_task.Task_Response])
async def read_all_tasks(
    service: TaskServiceDep,
    offset: int = Query(default=0, ge=0),
    limit: int = Query(default=10, ge=1, le=100)  # máximo 100 por página
):
    return service.get_all(offset, limit)


@router.post("/create-user", status_code=201)
async def create_user(user: schemas_user.User_Create, service: UserServiceDep):
    return service.create(name=user.name, email=user.email, password=user.password)


@router.post("/users/{user_id}/task")
async def create_task_for_admin(task: schemas_task.Task_Create, service: TaskServiceDep):
    return service.create_admin(title=task.title, description=task.description, user_id=task.user_id)


@router.put("/update-user/{user_id}", status_code=200, response_model=schemas_user.User_Response)
async def update_user(user_id: int, user: schemas_user.User_Update, service: UserServiceDep):
    return service.update_admin(user_id=user_id, name=user.name, email=user.email, password=user.password)


@router.put("/update-task/{task_id}", status_code=200)
async def update_task(task_id: int, task: schemas_task.Task_Update, service: TaskServiceDep):
    return service.update_admin(task_id=task_id, title=task.title, description=task.description)


@router.delete("/users/{user_id}", status_code=204)
async def delete_user(user_id: int, service: UserServiceDep):
    return service.delete(user_id=user_id)


@router.delete("/delete-task/{task_id}", status_code=204)
async def delete_task(service: TaskServiceDep, task_id: int):
    return service.delete_admin(task_id=task_id)
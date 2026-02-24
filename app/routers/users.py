from fastapi import APIRouter, Depends
from app.database import SessionDep
from typing import Annotated
from app.dependencies import auth
import app.schemas.user_schemas as schemas_user
import app.schemas.task_schemas as schemas_task
import app.services.task_services as services_task
from app.services.user_services import UserService
from app.repositories.user_repository import UserRepository
from app.services.task_services import TaskService
from app.repositories.task_repository import TaskRepository

router = APIRouter(
    prefix="/users",
    tags=["users"],
)

def get_user_service(session: SessionDep) -> UserService:
    repo = UserRepository(session)        # concreto criado aqui
    return UserService(repo)              # service recebe a abstracao

UserServiceDep = Annotated[UserService, Depends(get_user_service)]


def get_task_service(session: SessionDep) -> TaskService:
    repo = TaskRepository(session)        # concreto criado aqui
    return TaskService(repo)              # service recebe a abstracao


TaskServiceDep = Annotated[TaskService, Depends(get_task_service)]

@router.get("/{user_id}/tasks", status_code=200)
async def get_tasks_for_user(service: TaskServiceDep, user_id: int):
    return service.get_per_user(user_id)


@router.get("/{user_id}", response_model=schemas_user.User_Response)
async def read_user(user_id: int, service: UserServiceDep):
    return service.get_by_id(user_id)


@router.get("/by-email/", response_model=schemas_user.User_Response)
async def read_user_by_email(email: str, service: UserServiceDep):
    return service.get_by_email(email)


@router.post("/{user_id}/tasks", status_code=201)
async def create_task_for_user(task: schemas_task.Task_Create, service: TaskServiceDep, user=Depends(auth.get_current_user)):
    return service.create(title=task.title, description=task.description, user_id=task.user_id, current_user_id=user.id)


@router.put("/update-user/{user_id}", status_code=200, response_model=schemas_user.User_Response)
async def update_user(user_id: int, user: schemas_user.User_Update, service: UserServiceDep, current_user=Depends(auth.get_current_user)):
    return service.update(user_id=user_id, name=user.name, email=user.email, password=user.password, current_user_id=current_user.id)


@router.delete("/delete-user/{user_id}", status_code=204)
async def delete_user(user_id: int, service: UserServiceDep, user=Depends(auth.get_current_user)):
    return service.delete_common(user_id=user_id, current_user_id=user.id)
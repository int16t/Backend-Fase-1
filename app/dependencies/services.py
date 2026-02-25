from fastapi import Depends
from app.database import SessionDep
from typing import Annotated
from app.services.user_services import UserService
from app.repositories.user_repository import UserRepository
from app.services.task_services import TaskService
from app.repositories.task_repository import TaskRepository


def get_user_service(session: SessionDep) -> UserService:
    repo = UserRepository(session)        
    return UserService(repo)              # service recebe a abstracao

UserServiceDep = Annotated[UserService, Depends(get_user_service)]


def get_task_service(session: SessionDep) -> TaskService:
    repo = TaskRepository(session)        
    return TaskService(repo)              # service recebe a abstracao


TaskServiceDep = Annotated[TaskService, Depends(get_task_service)]
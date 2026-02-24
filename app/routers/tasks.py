from app.database import SessionDep
from fastapi import APIRouter, Depends
from typing import Annotated
import app.schemas.task_schemas as schemas
from app.dependencies import auth
from app.services.task_services import TaskService
from app.repositories.task_repository import TaskRepository


router = APIRouter(
    prefix="/tasks",
    tags=["tasks"],
)


def get_task_service(session: SessionDep) -> TaskService:
    repo = TaskRepository(session)        # concreto criado aqui
    return TaskService(repo)              # service recebe a abstracao


TaskServiceDep = Annotated[TaskService, Depends(get_task_service)]


@router.get("/{task_id}")
async def read_task(task_id: int, service: TaskServiceDep):
    return service.get_by_id(task_id)


@router.get("/by-title/")
async def read_task_by_title(title: str, service: TaskServiceDep):
    return service.get_by_title(title)


@router.put("/update-task/{task_id}", status_code=200)
async def update_task(task_id: int, task: schemas.Task_Update, service: TaskServiceDep, user=Depends(auth.get_current_user)):
    return service.update(task_id=task_id, title=task.title, description=task.description, user_id=user.id)


@router.delete("/delete-task/{task_id}", status_code=204)
async def delete_task(service: TaskServiceDep, task_id: int, user=Depends(auth.get_current_user)):
    return service.delete_common(task_id=task_id, user_id=user.id)
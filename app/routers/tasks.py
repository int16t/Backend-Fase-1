from fastapi import APIRouter, Depends
from app.dependencies.services import TaskServiceDep
import app.schemas.task_schemas as schemas
from app.dependencies.authorization import verify_own_task
from app.models.model_tasks import Task

router = APIRouter(
    prefix="/tasks",
    tags=["tasks"],
)


@router.get("/{task_id}")
async def read_task(task_id: int, service: TaskServiceDep):
    return service.get_by_id(task_id)


@router.get("/by-title/")
async def read_task_by_title(title: str, service: TaskServiceDep):
    return service.get_by_title(title)


@router.put("/update-task/{task_id}", status_code=200)
async def update_task(task_id: int, task: schemas.Task_Update, service: TaskServiceDep, current_task: Task = Depends(verify_own_task)):
    return service.update(task_id=task_id, title=task.title, description=task.description)


@router.delete("/delete-task/{task_id}", status_code=204)
async def delete_task(service: TaskServiceDep, task_id: int, current_task: Task = Depends(verify_own_task)):
    return service.delete(task_id=task_id)
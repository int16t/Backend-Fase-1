from fastapi import APIRouter, Depends, HTTPException
from app.dependencies.services import TaskServiceDep
import app.schemas.task_schemas as schemas
from app.dependencies.authorization import verify_own_task
from app.dependencies.auth import get_current_user
from app.models.model_tasks import Task
from app.models.model_users import User

router = APIRouter(
    prefix="/tasks",
    tags=["tasks"],
)


@router.get("/{task_id}")
async def read_task(task_id: int, service: TaskServiceDep, current_user: User = Depends(verify_own_task)):
    return service.get_by_id(task_id)


@router.get("/by-title/")
async def read_task_by_title(title: str, service: TaskServiceDep, current_user: User = Depends(get_current_user)):
    task = service.get_by_title(title)
    if task.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="You can only view your own tasks!")
    return task


@router.put("/update-task/{task_id}", status_code=200)
async def update_task(task_id: int, task: schemas.Task_Update, service: TaskServiceDep, current_task: Task = Depends(verify_own_task)):
    return service.update(task_id=task_id, title=task.title, description=task.description)


@router.delete("/delete-task/{task_id}", status_code=204)
async def delete_task(service: TaskServiceDep, task_id: int, current_task: Task = Depends(verify_own_task)):
    return service.delete(task_id=task_id)
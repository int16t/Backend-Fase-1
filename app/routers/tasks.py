from app.database import SessionDep
from fastapi import APIRouter, Depends
import app.schemas.task_schemas as schemas
import app.services.task_services as service_task
from app.dependencies import auth
router = APIRouter(
    prefix="/tasks",
    tags=["tasks"],
)


@router.get("/{task_id}")
async def read_task(task_id: int, session: SessionDep):
    return service_task.get_by_id(session, task_id)


@router.get("/by-title/")
async def read_task_by_title(title: str, session: SessionDep):
    return service_task.get_by_title(session, title)


@router.put("/update-task/{task_id}", status_code=200)
async def update_task(task_id: int, task: schemas.Task_Update, session: SessionDep, user=Depends(auth.get_current_user)):
    return service_task.update(session, task_id=task_id, title=task.title, description=task.description, user_id=user.id)


@router.delete("/delete-task/{task_id}", status_code=204)
async def delete_task(session: SessionDep, task_id: int, user=Depends(auth.get_current_user)):
    return service_task.delete_common(session, task_id=task_id, user_id=user.id)
from app.database import SessionDep
from fastapi import APIRouter
import app.crud.crud_tasks as crud_tasks
import app.schemas.task_schemas as schemas

router = APIRouter(
    prefix="/tasks",
    tags=["tasks"],
)


@router.get("/{task_id}")
async def read_task(task_id: int, session: SessionDep):
    return crud_tasks.get_task_by_id(session, task_id=task_id)


@router.get("/by-title/")
async def read_task_by_title(title: str, session: SessionDep):
    return crud_tasks.get_task_by_title(session, title=title)


@router.put("/update-task/{task_id}", status_code=200)
async def update_task(task_id: int, task: schemas.Task_Update, session: SessionDep):
    return crud_tasks.update_task(session, task_id=task_id, title=task.title, description=task.description)


@router.delete("/delete-task/{task_id}", status_code=204)
async def delete_task(task_id: int, session: SessionDep):
    return crud_tasks.delete_task(session, task_id=task_id)
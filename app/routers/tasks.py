from typing_extensions import Annotated
from app.database import SessionDep
from fastapi import APIRouter, HTTPException, Query
import app.crud.crud_tasks as crud
import app.schemas.task_schemas as schemas

router = APIRouter(
    prefix="/tasks",
    tags=["tasks"],
)


@router.get("/")
async def read_tasks(
    session: SessionDep,
    offset: int = 0,
    limit: Annotated[int, Query(le=100)] = 100,
    ):
    tasks = crud.get_tasks(session, offset, limit)
    if not tasks:
        raise HTTPException(status_code=404, detail="No tasks found")
    return tasks


@router.get("/{task_id}")
async def read_task(task_id: int, session: SessionDep):
    id_task = crud.get_task_by_id(session, task_id)
    if not id_task:
        raise HTTPException(status_code=404, detail="Task not found")
    return id_task

@router.get("/by-title/")
async def read_task_by_title(title: str, session: SessionDep):
    task = crud.get_task_by_title(session, title)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@router.post("/create-task", status_code=201)
async def create_task(task: schemas.Task_Create, session: SessionDep):
    db_task = crud.create_task(session, title=task.title, description=task.description)
    if db_task.title == "":
        raise HTTPException(status_code=422)
    return db_task


@router.put("/update-task/{task_id}", status_code=200)
async def update_task(task_id: int, task: schemas.Task_Update, session: SessionDep):
    db_task = crud.update_task(session, task_id=task_id, title=task.title, description=task.description)
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")
    return db_task


@router.delete("/delete-task/{task_id}", status_code=204)
async def delete_task(task_id: int, session: SessionDep):
    deleted = crud.delete_task(session, task_id=task_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Task not found")
    pass
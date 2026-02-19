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
async def read_tasks(session: SessionDep):
    return crud.get_tasks(session)


@router.get("/{task_id}")
async def read_task(task_id: int, session: SessionDep):
    return crud.get_task_by_id(session, task_id=task_id)

@router.get("/by-title/")
async def read_task_by_title(title: str, session: SessionDep):
    return crud.get_task_by_title(session, title=title)


@router.post("/create-task", status_code=201)
async def create_task(task: schemas.Task_Create, session: SessionDep):
    return crud.create_task(session, title=task.title, description=task.description)


@router.put("/update-task/{task_id}", status_code=200)
async def update_task(task_id: int, task: schemas.Task_Update, session: SessionDep):
    return crud.update_task(session, task_id=task_id, title=task.title, description=task.description)


@router.delete("/delete-task/{task_id}", status_code=204)
async def delete_task(task_id: int, session: SessionDep):
    return crud.delete_task(session, task_id=task_id)
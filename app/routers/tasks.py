from typing_extensions import Annotated
from app.database import SessionDep
from app.models.model_tasks import Task
from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel, Field
from sqlmodel import select
import app.crud.crud_tasks as crud


router = APIRouter(
    prefix="/tasks",
    tags=["tasks"],
)

class Task_base(BaseModel):
    id: int
    title: str = Field(min_length=1, max_length=100)
    description: str = Field(min_length=1, max_length=200)

class Task_response(BaseModel):
    title: str = Field(min_length=1, max_length=100)
    description: str = Field(min_length=1, max_length=200)


@router.get("/")
async def read_tasks(
    session: SessionDep,
    offset: int = 0,
    limit: Annotated[int, Query(le=100)] = 100,
    ):
    tasks = crud.get_tasks(session, offset, limit)
    return tasks


@router.get("/{task_id}")
async def read_task(task_id: int, session: SessionDep):
    id_task = crud.get_task_by_id(session, task_id)
    return id_task if id_task else HTTPException(status_code=404, detail="Task not found")


@router.post("/create-task", status_code=201)
async def create_task(task: Task_response, session: SessionDep) -> Task_response:
    db_task = crud.create_task(session, title=task.title, description=task.description)
    return db_task


@router.put("/update-task/{task_id}", status_code=200)
async def update_task(task_id: int, task: Task_response, session: SessionDep) -> Task_response:
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
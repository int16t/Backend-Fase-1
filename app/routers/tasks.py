from typing_extensions import Annotated
from app.database import SessionDep
from app.models.model_tasks import Task
from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel, Field
from sqlmodel import select

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
    ) -> list[Task_base]:
    tasks = session.exec(select(Task).offset(offset).limit(limit)).all()
    return [Task_base(id=task.id, title=task.title, description=task.description) for task in tasks]


@router.get("/{task_id}")
async def read_task(task_id: int, session: SessionDep):
    task = session.get(Task, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@router.post("/create-task", status_code=201)
async def create_task(task: Task_response, session: SessionDep) -> Task_response:
    db_task = Task(title=task.title, description=task.description)
    session.add(db_task)
    session.commit()
    session.refresh(db_task)
    return Task_response(title=db_task.title, description=db_task.description)


@router.put("/update-task/{task_id}", status_code=200)
async def update_task(task_id: int, task: Task_response, session: SessionDep) -> Task_response:
    db_task = session.get(Task, task_id)
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")
    db_task.title = task.title
    db_task.description = task.description
    session.commit()
    session.refresh(db_task)
    return Task_response(title=db_task.title, description=db_task.description)

@router.delete("/delete-task/{task_id}", status_code=204)
async def delete_task(task_id: int, session: SessionDep):
    task = session.get(Task, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    session.delete(task)
    session.commit()
    pass



from sqlmodel import Session, select
from app.models.model_tasks import Task
from app.exceptions import NotFound


def get_tasks(session: Session, offset: int = 0, limit: int = 100) -> list[Task]:
    tasks = session.exec(select(Task).offset(offset).limit(limit)).all()
    if not tasks:
        raise NotFound(name="Tasks")
    return tasks


def get_task_by_id(session: Session, task_id: int) -> Task | None:
    db_task = session.get(Task, task_id)
    if not db_task:
        raise NotFound(name="Task")
    return db_task


def get_task_by_title(session: Session, title: str) -> Task | None:
    db_task = session.exec(select(Task).where(Task.title == title)).first()
    if not db_task:
        raise NotFound(name="Task")
    return db_task


def create_task(session: Session, title: str, description: str) -> Task:
    db_task = Task(title=title, description=description)
    if db_task.title == "":
        raise ValueError("Title cannot be empty")
    session.add(db_task)
    session.commit()
    session.refresh(db_task)
    return db_task


def update_task(session: Session, task_id: int, title: str, description: str) -> Task | None:
    db_task = session.get(Task, task_id)
    if not db_task:
        raise NotFound(name="Task")
    db_task.title = title
    db_task.description = description
    session.commit()
    session.refresh(db_task)
    return db_task


def delete_task(session: Session, task_id: int) -> bool:
    db_task = session.get(Task, task_id)
    if not db_task:
        raise NotFound(name="Task")
    session.delete(db_task)
    session.commit()
    return bool(db_task)
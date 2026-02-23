from sqlmodel import Session, select
from app.models.model_tasks import Task


def get_all(session: Session, offset: int = 0, limit: int = 100) -> list[Task]:
    return list(session.exec(select(Task).order_by(Task.id).offset(offset).limit(limit)).all())

def get_by_id(session: Session, task_id: int) -> Task | None:
    return session.get(Task, task_id)

def get_task_by_title(session: Session, title: str) -> Task | None:
    return session.exec(select(Task).where(Task.title == title)).first()

def get_tasks_per_user(session: Session, user_id: int, offset: int = 0, limit: int = 100) -> list[Task]:
    return session.exec(select(Task).where(Task.user_id == user_id).offset(offset).limit(limit)).all()
    
def save(session: Session, task: Task) -> Task:
    session.add(task)
    session.commit()
    session.refresh(task)
    return task

def update(session: Session, task: Task) -> Task:
    session.commit()
    session.refresh(task)
    return task

def delete(session: Session, task: Task):
    session.delete(task)
    session.commit()
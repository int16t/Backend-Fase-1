from sqlmodel import Session, select
from app.models.model_tasks import Task
from app.interfaces.i_task_repository import ITaskRepository

class TaskRepository(ITaskRepository):

    def __init__(self, session: Session):
        self.session = session

    def get_all(self, offset: int = 0, limit: int = 100) -> list[Task]:
        return list(self.session.exec(
            select(Task).order_by(Task.id).offset(offset).limit(limit)
            ).all())

    def get_by_id(self, task_id: int) -> Task | None:
        return self.session.get(Task, task_id)

    def get_task_by_title(self, title: str) -> Task | None:
        return self.session.exec(
            select(Task).where(Task.title == title)
            ).first()

    def get_tasks_per_user(self, user_id: int, offset: int = 0, limit: int = 100) -> list[Task]:
        return self.session.exec(
            select(Task).where(Task.user_id == user_id).offset(offset).limit(limit)
            ).all()
        
    def save(self, task: Task) -> Task:
        self.session.add(task)
        self.session.commit()
        self.session.refresh(task)
        return task

    def update(self, task: Task) -> Task:
        self.session.commit()
        self.session.refresh(task)
        return task

    def delete(self, task: Task):
        self.session.delete(task)
        self.session.commit()
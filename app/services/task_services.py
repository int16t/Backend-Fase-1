from sqlmodel import Session
from app.models.model_tasks import Task
from app.repositories import task_repository
import app.exceptions as exceptions


def get_all(session: Session, offset: int = 0, limit: int = 100) -> list[Task]:
    return task_repository.get_all(session, offset, limit)


def get_by_id(session: Session, task_id: int) -> Task:
    task = task_repository.get_by_id(session, task_id)
    if not task:
        raise exceptions.NotFound(name="Task")
    return task


def get_by_title(session: Session, title: str)-> Task:
    task = task_repository.get_task_by_title(session, title)
    if not task:
        raise exceptions.NotFound(name="Task")
    return task


def get_per_user(session: Session, user_id: int)-> list[Task]:
    tasks = task_repository.get_tasks_per_user(session, user_id)
    if not tasks:
        raise exceptions.NotFound(name="Tasks")
    return tasks


def create(session: Session, title: str, description: str, user_id: int, current_user_id: int) -> Task:
    if user_id != current_user_id:
        raise exceptions.NotAllowed("You can only create tasks for your own user!")
    task = Task(title=title, description=description, user_id=user_id)
    return task_repository.save(session, task)


def create_admin(session: Session, title: str, description: str, user_id: int) -> Task:
    # Admins can create tasks for any user without ownership check
    task = Task(title=title, description=description, user_id=user_id)
    return task_repository.save(session, task)


def update(session: Session, title: str, description: str, task_id: int, user_id: int) -> Task:
    task = task_repository.get_by_id(session, task_id)
    if not task:
        raise exceptions.NotFound(name="Task")
    if task.user_id != user_id:
        raise exceptions.NotAllowed("You can only update your own tasks!")
    task.title = title
    task.description = description
    return task_repository.update(session, task)


def update_admin(session: Session, title: str, description: str, task_id: int) -> Task:
    task = task_repository.get_by_id(session, task_id)
    if not task:
        raise exceptions.NotFound(name="Task")
    task.title = title
    task.description = description
    task.id = task_id
    return task_repository.update(session, task)


def delete_admin(session: Session, task_id: int):
    task = task_repository.get_by_id(session, task_id)
    if not task:
        raise exceptions.NotFound(name="Task")
    return task_repository.delete(session, task)


def delete_common(session: Session, task_id: int, user_id: int):
    task = task_repository.get_by_id(session, task_id)
    if not task:
        raise exceptions.NotFound(name="Task")
    if task.user_id != user_id:
        raise exceptions.NotAllowed("You can only delete your own tasks!")
    task_repository.delete(session, task)
    return True
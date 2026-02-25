from app.models.model_tasks import Task
import app.exceptions as exceptions
from app.interfaces.i_task_repository import ITaskRepository


class TaskService:

    def __init__(self, repo:ITaskRepository):
        self.repo = repo


    def get_all(self, offset: int = 0, limit: int = 100) -> list[Task]:
        return self.repo.get_all(offset, limit)


    def get_by_id(self, task_id: int) -> Task:
        task = self.repo.get_by_id(task_id)
        if not task:
            raise exceptions.NotFound(name="Task")
        return task


    def get_by_title(self, title: str)-> Task:
        task = self.repo.get_task_by_title(title)
        if not task:
            raise exceptions.NotFound(name="Task")
        return task


    def get_per_user(self, user_id: int)-> list[Task]:
        tasks = self.repo.get_tasks_per_user(user_id)
        if not tasks:
            raise exceptions.NotFound(name="Tasks")
        return tasks


    def create(self, title: str, description: str, user_id: int) -> Task:
        task = Task(title=title, description=description, user_id=user_id)
        return self.repo.save(task)


    def update(self, title: str, description: str, task_id: int) -> Task:
        task = self.repo.get_by_id(task_id)
        if not task:
            raise exceptions.NotFound(name="Task")
        task.title = title
        task.description = description
        return self.repo.update(task)


    def delete(self, task_id: int):
        task = self.repo.get_by_id(task_id)
        if not task:
            raise exceptions.NotFound(name="Task")
        return self.repo.delete(task)
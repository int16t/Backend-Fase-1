from abc import ABC, abstractmethod
from app.models.model_tasks import Task

class ITaskRepository(ABC):

    @abstractmethod
    def get_all(self, offset: int = 0, limit: int = 100) -> list[Task]: ...

    @abstractmethod
    def get_by_id(self, task_id: int) -> Task | None: ...

    @abstractmethod
    def get_task_by_title(self, title: str) -> Task | None: ...

    @abstractmethod
    def get_tasks_per_user(self, user_id: int, offset: int = 0, limit: int = 100) -> list[Task]: ...

    @abstractmethod
    def save(self, task: Task) -> Task: ...

    @abstractmethod
    def update(self, task: Task) -> Task: ...

    @abstractmethod
    def delete(self, task: Task) -> None: ...

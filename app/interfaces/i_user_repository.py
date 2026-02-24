from abc import ABC, abstractmethod
from app.models.model_users import User

class IUserRepository(ABC):

    @abstractmethod
    def get_all(self, offset: int = 0, limit: int = 100) -> list[User]: ...

    @abstractmethod
    def get_by_id(self, user_id: int) -> User | None: ...

    @abstractmethod
    def get_by_email(self, email: str) -> User | None: ...

    @abstractmethod
    def get_by_name(self, name: str, offset: int = 0, limit: int = 100) -> list[User]: ...

    @abstractmethod
    def save(self, user: User) -> User: ...

    @abstractmethod
    def update(self, user: User) -> User: ...

    @abstractmethod
    def delete(self, user: User) -> None: ...

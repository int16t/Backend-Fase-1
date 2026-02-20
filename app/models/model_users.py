from sqlmodel import SQLModel, Field, Relationship
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.model_tasks import Task

class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    email: str | None = Field(index=True)
    tasks: list["Task"] = Relationship(back_populates="owner")
    password_hash: str
    is_admin: bool = False
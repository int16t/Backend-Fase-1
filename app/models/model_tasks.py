from sqlmodel import SQLModel, Field, Relationship
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.model_users import User

class Task(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    title: str = Field(index=True)
    description: str | None = Field(index=True)
    user_id: int | None = Field(default=None, foreign_key="user.id")
    owner: "User" = Relationship(back_populates="tasks")
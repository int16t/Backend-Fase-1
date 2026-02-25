from pydantic import BaseModel, EmailStr, Field, field_validator
import re


class User_Create(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    email: EmailStr = Field(min_length=1, max_length=30)
    password: str = Field(min_length=8, max_length=128)

    @field_validator("password")
    @classmethod
    def password_strength(cls, v: str) -> str:
        if not re.search(r"[A-Za-z]", v):
            raise ValueError("The password must have at least one letter")
        if not re.search(r"\d", v):
            raise ValueError("The password must have at least one number")
        return v

class User_Update(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    email: EmailStr = Field(min_length=1, max_length=30)
    password: str = Field(min_length=8, max_length=128)

    @field_validator("password")
    @classmethod
    def password_strength(cls, v: str) -> str:
        if not re.search(r"[A-Za-z]", v):
            raise ValueError("The password must have at least one letter")
        if not re.search(r"\d", v):
            raise ValueError("The password must have at least one number")
        return v

class User_Response(BaseModel):
    id: int
    name: str = Field(min_length=1, max_length=100)
    email: EmailStr = Field(min_length=1, max_length=30)
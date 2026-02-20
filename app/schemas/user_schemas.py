from pydantic import BaseModel, EmailStr, Field


class User_Create(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    email: EmailStr = Field(min_length=1, max_length=30)
    password: str

class User_Update(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    email: EmailStr = Field(min_length=1, max_length=30)

class User_Response(BaseModel):
    id: int
    name: str = Field(min_length=1, max_length=100)
    email: EmailStr = Field(min_length=1, max_length=30)
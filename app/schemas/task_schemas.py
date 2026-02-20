from pydantic import BaseModel, Field, field_validator

class Task_Create(BaseModel):
    title: str = Field(min_length=1, max_length=100)
    description: str = Field(min_length=1, max_length=200)
    user_id: int

    @field_validator("title", "description")
    @classmethod
    def not_blank(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("Field cannot be blank or whitespace only")
        return value.strip()  


class Task_Update(BaseModel): 
    title: str = Field(min_length=1, max_length=100)
    description: str = Field(min_length=1, max_length=200)
    user_id: int

    @field_validator("title", "description")
    @classmethod
    def not_blank(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("Field cannot be blank or whitespace only")
        return value.strip()
    

class Task_Response(BaseModel):
    id: int
    title: str = Field(min_length=1, max_length=100)
    description: str = Field(min_length=1, max_length=200)
    user_id: int

    @field_validator("title", "description")
    @classmethod
    def not_blank(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("Field cannot be blank or whitespace only")
        return value.strip()
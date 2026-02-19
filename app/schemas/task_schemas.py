from pydantic import BaseModel, Field

class Task_Create(BaseModel):
    title: str = Field(min_length=1, max_length=100)
    description: str = Field(min_length=1, max_length=200)

class Task_Update(BaseModel): 
    title: str = Field(min_length=1, max_length=100)
    description: str = Field(min_length=1, max_length=200)

class Task_Response(BaseModel):
    id: int
    title: str = Field(min_length=1, max_length=100)
    description: str = Field(min_length=1, max_length=200)
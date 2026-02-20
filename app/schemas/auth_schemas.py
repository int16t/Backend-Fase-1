from pydantic import BaseModel, EmailStr, Field


class Login_Request(BaseModel):
    email: EmailStr
    password: str


class RegisterRequest(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    email: EmailStr = Field(min_length=1, max_length=30)
    password: str
    

class Token_Response(BaseModel):
    access_token: str
    token_type: str = "bearer"
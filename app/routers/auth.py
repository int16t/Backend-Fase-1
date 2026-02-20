from fastapi import APIRouter, HTTPException
from app.database import SessionDep
from app.schemas.auth_schemas import Login_Request, RegisterRequest, Token_Response
from app.schemas.user_schemas import User_Response
from app.crud import crud_users
from app.auth import auth

router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)

@router.post("/register", status_code=201, response_model=User_Response)
async def register_user(data: RegisterRequest, session: SessionDep):
    return crud_users.create_user(session, data.name, data.email, data.password)


@router.post("/login", response_model=Token_Response)
async def validate_user(data: Login_Request, session: SessionDep):
    user = crud_users.get_user_by_email(session, email=data.email)

    if not auth.verify_password(data.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = auth.create_access_token(data={"sub": str(user.id)})
    return Token_Response(access_token=token)
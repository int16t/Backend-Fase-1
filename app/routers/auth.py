from fastapi import APIRouter, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import Depends
from app.database import SessionDep
from app.schemas.auth_schemas import RegisterRequest, Token_Response
from app.schemas.user_schemas import User_Response
from app.crud import crud_users
from app.services import user_services
from app.auth import auth

router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)


@router.post("/register", status_code=201, response_model=User_Response)
async def register_user(data: RegisterRequest, session: SessionDep):
    return user_services.create(session, data.name, data.email, data.password)


@router.post("/login", response_model=Token_Response)
async def validate_user(session: SessionDep, form_data: OAuth2PasswordRequestForm = Depends()):
    user = user = user_services.get_by_email(session, email=form_data.username)

    if not auth.verify_password(form_data.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = auth.create_access_token(data={"sub": str(user.id)})
    return Token_Response(access_token=token)
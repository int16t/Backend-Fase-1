from fastapi import APIRouter, HTTPException, Depends, Request
from fastapi.security import OAuth2PasswordRequestForm
from app.schemas.auth_schemas import RegisterRequest, Token_Response
from app.schemas.user_schemas import User_Response
from app.dependencies.services import UserServiceDep
from app.auth import auth
from app.limiter import limiter


router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)


@router.post("/register", status_code=201, response_model=User_Response)
@limiter.limit("5/minute")
async def register_user(request: Request, data: RegisterRequest, service: UserServiceDep):
    return service.create(data.name, data.email, data.password)


@router.post("/login", response_model=Token_Response)
@limiter.limit("5/minute")
async def validate_user(request: Request, service: UserServiceDep, form_data: OAuth2PasswordRequestForm = Depends()):
    user = service.get_by_email(email=form_data.username)

    if not auth.verify_password(form_data.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = auth.create_access_token(data={"sub": str(user.id)})
    return Token_Response(access_token=token)
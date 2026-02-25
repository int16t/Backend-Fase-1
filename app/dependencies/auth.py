from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from app.models.model_users import User
from app.auth import auth
from app.dependencies.services import UserServiceDep


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def get_current_user(service: UserServiceDep, token: str = Depends(oauth2_scheme)) -> User:
    payload = auth.decode_access_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    user_id = payload.get("sub")
    user_id = int(user_id)
    user = service.get_by_id(user_id)
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    return user

def require_admin(current_user: User = Depends(get_current_user)) -> User:
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Admin access required")
    return current_user
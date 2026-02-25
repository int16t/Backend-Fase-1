from fastapi import Depends, HTTPException
from app.models.model_users import User
from app.dependencies.auth import get_current_user
from app.dependencies.services import TaskServiceDep

def verify_own_user(
    user_id: int,
    current_user: User = Depends(get_current_user)
) -> User:
    if user_id != current_user.id:
        raise HTTPException(status_code=403, detail="You can only modify your own user!")
    return current_user

def verify_own_task(
    task_id: int,
    service: TaskServiceDep,
    current_user: User = Depends(get_current_user)
    ) -> User:
    task = service.get_by_id(task_id)
    if task.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="You can only modify your own tasks!")
    return current_user

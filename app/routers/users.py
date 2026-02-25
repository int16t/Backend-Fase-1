from fastapi import APIRouter, Depends
from app.dependencies.services import TaskServiceDep, UserServiceDep
import app.schemas.user_schemas as schemas_user
import app.schemas.task_schemas as schemas_task
from app.models.model_users import User
from app.dependencies.authorization import verify_own_user


router = APIRouter(
    prefix="/users",
    tags=["users"],
)


@router.get("/{user_id}/tasks", status_code=200)
async def get_tasks_for_user(service: TaskServiceDep, user_id: int):
    return service.get_per_user(user_id)


@router.get("/{user_id}", response_model=schemas_user.User_Response)
async def read_user(user_id: int, service: UserServiceDep):
    return service.get_by_id(user_id)


@router.get("/by-email/", response_model=schemas_user.User_Response)
async def read_user_by_email(email: str, service: UserServiceDep):
    return service.get_by_email(email)


@router.post("/{user_id}/tasks", status_code=201)
async def create_task_for_user(task: schemas_task.Task_Create, service: TaskServiceDep, current_user: User = Depends(verify_own_user)):
    return service.create(title=task.title, description=task.description, user_id=task.user_id)


@router.put("/update-user/{user_id}", status_code=200, response_model=schemas_user.User_Response)
async def update_user(user_id: int, user: schemas_user.User_Update, service: UserServiceDep, current_user: User = Depends(verify_own_user)):
    return service.update(user_id=user_id, name=user.name, email=user.email, password=user.password)


@router.delete("/delete-user/{user_id}", status_code=204)
async def delete_user(user_id: int, service: UserServiceDep, current_user: User = Depends(verify_own_user)):
    return service.delete(user_id=user_id)
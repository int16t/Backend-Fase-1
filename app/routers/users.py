from fastapi import APIRouter, Depends
from app.database import SessionDep
import app.schemas.user_schemas as schemas_user
import app.schemas.task_schemas as schemas_task
import app.services.task_services as services_task
import app.services.user_services as services_user
from app.dependencies import auth

router = APIRouter(
    prefix="/users",
    tags=["users"],
)

@router.get("/{user_id}/tasks", status_code=200)
async def get_tasks_for_user(session: SessionDep, user_id: int):
    return services_task.get_per_user(session, user_id)


@router.get("/{user_id}", response_model=schemas_user.User_Response)
async def read_user(user_id: int, session: SessionDep):
    return services_user.get_by_id(session, user_id=user_id)


@router.get("/by-email/", response_model=schemas_user.User_Response)
async def read_user_by_email(email: str, session: SessionDep):
    return services_user.get_by_email(session, email=email)


@router.post("/{user_id}/tasks", status_code=201)
async def create_task_for_user(task: schemas_task.Task_Create, session: SessionDep, user=Depends(auth.get_current_user)):
    return services_task.create(session, title=task.title, description=task.description, user_id=task.user_id, current_user_id=user.id)


@router.put("/update-user/{user_id}", status_code=200, response_model=schemas_user.User_Response)
async def update_user(user_id: int, user: schemas_user.User_Update, session: SessionDep, current_user=Depends(auth.get_current_user)):
    return services_user.update(session, user_id=user_id, name=user.name, email=user.email, password=user.password, current_user_id=current_user.id)


@router.delete("/delete-user/{user_id}", status_code=204)
async def delete_user(user_id: int, session: SessionDep, user=Depends(auth.get_current_user)):
    return services_user.delete_common(session, user_id=user_id, current_user_id=user.id)
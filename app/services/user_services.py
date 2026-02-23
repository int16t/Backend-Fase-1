from sqlmodel import Session, select
from app.models.model_users import User
from app.repositories import user_repository
import app.exceptions as exceptions
from app.auth import auth


def get_all(session: Session, offset: int = 0 , limit: int = 100) -> list[User]:
    return user_repository.get_all(session, offset, limit)


def get_by_id(session: Session, user_id: int)-> User | None:
    user = user_repository.get_by_id(session, user_id)
    if not user:
        raise exceptions.NotFound(name="User")
    return user


def get_by_email(session: Session, email: str)-> User| None:
    user = user_repository.get_by_email(session, email)
    if not user:
        raise exceptions.NotFound(name="User")
    return user


def get_by_name(session: Session, name: str, offset: int = 0, limit: int = 100)-> list[User]:
    return user_repository.get_by_name(session, name, offset, limit)
    

def create(session: Session, name: str, email: str, password: str)-> User:
    existing = user_repository.get_by_email(session, email)
    if existing:
        raise exceptions.EmailAlreadyExistsError(email=email)
    password_hash = auth.hash_password(password)
    user = User(name=name, email=email, password_hash=password_hash)
    return user_repository.save(session, user)


def update(session: Session, name: str, email: str, password: str, user_id, current_user_id: int)-> User:
    if user_id != current_user_id:
        raise exceptions.NotAllowed("You can only update your own user!")
    user = user_repository.get_by_id(session, user_id)
    if not user:
        raise exceptions.NotFound(name="User")
    user.name = name
    user.email = email
    verify = auth.verify_password(password, user.password_hash)
    if not verify:
        password_hash = auth.hash_password(password)
        user.password_hash = password_hash
    return user_repository.update(session, user)


def update_admin(session: Session, name: str, email: str, password: str, user_id)-> User:
    user = user_repository.get_by_id(session, user_id)
    if not user:
        raise exceptions.NotFound(name="User")
    user.name = name
    user.email = email
    verify = auth.verify_password(password, user.password_hash)
    if not verify:
        password_hash = auth.hash_password(password)
        user.password_hash = password_hash
    return user_repository.update(session, user)


def delete_common(session: Session, user_id: int, current_user_id: int):
    if user_id != current_user_id:
        raise exceptions.NotAllowed("You can only delete your own user!")
    user = user_repository.get_by_id(session, user_id)
    if not user:
        raise exceptions.NotFound(name="User")
    return user_repository.delete(session, user)


def delete(session: Session, user_id: int):
    user = user_repository.get_by_id(session, user_id)
    if not user:
        raise exceptions.NotFound(name="User")
    return user_repository.delete(session, user)
from sqlmodel import Session, select
from app.models.model_users import User
import app.exceptions as exceptions


def get_users(session: Session, offset: int = 0, limit: int = 100) -> list[User]:
    users = session.exec(select(User).offset(offset).limit(limit)).all()
    if not users:
        raise exceptions.NotFound(name="Users")
    return users


def get_user_by_id(session: Session, user_id: int) -> User | None:
    db_user = session.get(User, user_id)
    if not db_user:
        raise exceptions.NotFound(name="User")
    return db_user


def get_user_by_email(session: Session, email: str) -> User | None:
    db_user = session.exec(select(User).where(User.email == email)).first()
    if not db_user:
        raise exceptions.NotFound(name="User")
    return db_user


def create_user(session: Session, name: str, email: str) -> User:
    existing = session.exec(select(User).where(User.email == email)).first()
    if existing:
        raise exceptions.EmailAlreadyExistsError(email=email)
    db_user = User(name=name, email=email)
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user


def update_user(session: Session, user_id: int, name: str, email: str) -> User | None:
    db_user = session.get(User, user_id)
    if not db_user:
        raise exceptions.NotFound(name="User")
    db_user.name = name
    db_user.email = email
    session.commit()
    session.refresh(db_user)
    return db_user


def delete_user(session: Session, user_id: int) -> bool:
    db_user = session.get(User, user_id)
    if not db_user:
        raise exceptions.NotFound(name="User")
    session.delete(db_user)
    session.commit()
    return bool(db_user)
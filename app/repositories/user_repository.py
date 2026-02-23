from sqlmodel import Session, select
from app.models.model_users import User


def get_all(session: Session, offset: int = 0, limit: int = 100)-> list[User]:
    return list(session.exec(select(User).order_by(User.id).offset(offset).limit(limit)).all())

def get_by_id(session: Session, user_id: int) -> User | None:
    return session.get(User, user_id)

def get_by_email(session: Session, email: str) -> User | None:
    return session.exec(select(User).where(User.email == email)).first()

def get_by_name(session: Session, name: str, offset: int = 0, limit: int = 100) -> list[User]:
    return list(session.exec(select(User).order_by(User.id).where(User.name == name).offset(offset).limit(limit)).all)

def save(session: Session, user: User) -> User:
    session.add(user)
    session.commit()
    session.refresh(user)
    return user

def update(session: Session, user: User) -> User:
    session.commit()
    session.refresh(user)
    return user

def delete(session: Session, user: User):
    session.delete(user)
    session.commit()




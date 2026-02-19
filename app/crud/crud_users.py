from sqlmodel import Session, select
from app.models.model_users import User


def get_users(session: Session, offset: int = 0, limit: int = 100) -> list[User]:
    """Retorna lista de usuários com paginação."""
    return session.exec(select(User).offset(offset).limit(limit)).all()


def get_user_by_id(session: Session, user_id: int) -> User | None:
    """Retorna um usuário pelo ID ou None se não existir."""
    return session.get(User, user_id)


def get_user_by_email(session: Session, email: str) -> User | None:
    """Retorna um usuário pelo email ou None se não existir."""
    return session.exec(select(User).where(User.email == email)).first()


def create_user(session: Session, name: str, email: str) -> User:
    """Cria um novo usuário no banco de dados."""
    db_user = User(name=name, email=email)
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user


def update_user(session: Session, user_id: int, name: str, email: str) -> User | None:
    """Atualiza um usuário existente. Retorna None se não encontrar."""
    db_user = session.get(User, user_id)
    if not db_user:
        return None
    db_user.name = name
    db_user.email = email
    session.commit()
    session.refresh(db_user)
    return db_user


def delete_user(session: Session, user_id: int) -> bool:
    """Deleta um usuário. Retorna True se deletou, False se não encontrou."""
    db_user = session.get(User, user_id)
    if not db_user:
        return False
    session.delete(db_user)
    session.commit()
    return True
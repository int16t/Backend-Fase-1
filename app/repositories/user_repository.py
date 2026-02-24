from sqlmodel import Session, select
from app.models.model_users import User
from app.interfaces.i_user_repository import IUserRepository

class UserRepository(IUserRepository):

    def __init__(self, session: Session):
        self.session = session

    def get_all(self, offset: int = 0, limit: int = 100)-> list[User]:
        return list(self.session.exec(
            select(User).order_by(User.id).offset(offset).limit(limit)
            ).all())

    def get_by_id(self, user_id: int) -> User | None:
        return self.session.get(User, user_id)

    def get_by_email(self, email: str) -> User | None:
        return self.session.exec(select(User).where(User.email == email)).first()

    def get_by_name(self, name: str, offset: int = 0, limit: int = 100) -> list[User]:
        return list(self.session.exec(
            select(User).order_by(User.id).where(User.name == name).offset(offset).limit(limit)
            ).all())

    def save(self, user: User) -> User:
        self.session.add(user)
        self.session.commit()
        self.session.refresh(user)
        return user

    def update(self, user: User) -> User:
        self.session.commit()
        self.session.refresh(user)
        return user

    def delete(self, user: User):
        self.session.delete(user)
        self.session.commit()




from app.interfaces.i_user_repository import IUserRepository
from app.models.model_users import User 
import app.exceptions as exceptions
from app.auth import auth

class UserService:

    def __init__(self, repo:IUserRepository):
        self.repo = repo


    def get_all(self, offset: int = 0 , limit: int = 100) -> list[User]:
        return self.repo.get_all(offset, limit)


    def get_by_id(self, user_id: int)-> User | None:
        user = self.repo.get_by_id(user_id)
        if not user:
            raise exceptions.NotFound(name="User")
        return user


    def get_by_email(self, email: str)-> User| None:
        user = self.repo.get_by_email(email)
        if not user:
            raise exceptions.NotFound(name="User")
        return user


    def get_by_name(self, name: str, offset: int = 0, limit: int = 100)-> list[User]:
        return self.repo.get_by_name(name, offset, limit)
        

    def create(self, name: str, email: str, password: str)-> User:
        existing = self.repo.get_by_email(email)
        if existing:
            raise exceptions.EmailAlreadyExistsError(email=email)
        password_hash = auth.hash_password(password)
        user = User(name=name, email=email, password_hash=password_hash)
        return self.repo.save(user)


    def update(self, name: str, email: str, password: str, user_id)-> User:
        user = self.repo.get_by_id(user_id)
        if not user:
            raise exceptions.NotFound(name="User")
        user.name = name
        user.email = email
        verify = auth.verify_password(password, user.password_hash)
        if not verify:
            password_hash = auth.hash_password(password)
            user.password_hash = password_hash
        return self.repo.update(user)


    def delete(self, user_id: int):
        user = self.repo.get_by_id(user_id)
        if not user:
            raise exceptions.NotFound(name="User")
        return self.repo.delete(user)
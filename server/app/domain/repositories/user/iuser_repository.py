from abc import abstractmethod
from sqlalchemy.orm import Session

from app.domain.models.user import User
from app.domain.enums.role import Role

class IUserRepository:
    @abstractmethod
    def get_all(self, db: Session)-> list[User]:
        pass

    @abstractmethod
    def get_by_id(self, user_id: int, db: Session)-> User | None:
        pass

    @abstractmethod
    def get_by_email(self, email: str, db: Session)-> User | None:
        pass
    
    @abstractmethod
    def create(self, user: User)-> User:
        pass

    @abstractmethod
    def delete_user(self, user: User, db: Session)-> None:
        pass

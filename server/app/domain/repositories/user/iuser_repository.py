from abc import ABC, abstractmethod
from sqlalchemy.orm import Session

from app.domain.models.user import User

class IUserRepository(ABC):
    @abstractmethod
    def get_all(self, db: Session) -> list[User]:
        pass

    @abstractmethod
    def get_by_id(self, user_id: int, db: Session) -> User | None:
        pass

    @abstractmethod
    def get_by_email(self, email: str, db: Session) -> User | None:
        pass
    
    @abstractmethod
    def create(self, user: User, db: Session) -> User:
        pass

    @abstractmethod
    def delete_user(self, user: User, db: Session) -> None:
        pass

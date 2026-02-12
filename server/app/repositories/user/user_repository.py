from sqlalchemy.orm import Session

from app.domain.models.user import User
from app.domain.repositories.user.iuser_repository import IUserRepository

class UserRepository(IUserRepository):
    def get_all(self, db: Session)-> list[User]:
        return db.query(User).all()

    def get_by_id(self, user_id: int, db: Session)-> User | None:
        return db.query(User).filter(User.user_id == user_id).first()

    def get_by_ids(self, user_ids: list[int], db: Session) -> list[User]:
        if not user_ids:
            return []
        
        users = db.query(User).filter(User.user_id.in_(user_ids)).all()
        return users
        
    def get_by_email(self, email: str, db: Session)-> User | None:
        return db.query(User).filter(User.email == email).first()
    
    def create(self, user: User, db: Session)-> User:
        db.add(user)
        db.flush()
        db.refresh(user)
        return user

    def delete_user(self, user: User, db: Session)-> None:
        db.delete(user)
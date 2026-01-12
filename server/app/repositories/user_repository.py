from sqlalchemy.orm import Session
from app.domain.models.User import User
from app.domain.enums.Role import Role
from app.domain.repositories.iuser_repository import IUserRepository

class UserRepository(IUserRepository):
    def get_all(self, db: Session)-> list[User]:
        return db.query(User).all()

    def get_by_id(self, user_id: int, db: Session)-> User | None:
        return db.query(User).filter(User.user_id == user_id).first()

    def get_by_email(self, email: str, db: Session)-> User | None:
        return db.query(User).filter(User.email == email).first()
    
    def create(self, user: User, db: Session)-> User:
        db.add(user)
        db.flush()
        db.refresh(user)
        return user

    def update_user_role(self, user: User, user_role: Role, db: Session)-> None:
        user.role = user_role
        db.flush()

    def delete_user(self, user: User, db: Session)-> None:
        db.delete(user)
        db.flush()

from app.database import get_db, get_db_transaction
from app.domain.dtos.user.update_user_dto import UpdateUserDTO
from app.domain.services.iuser_service import IUserService
from app.domain.types.Result import ok, err, Result
from app.domain.models.User import User
from app.domain.enums.Role import Role
from app.domain.enums.ErrorType import ErrorType
from app.domain.repositories.iuser_repository import IUserRepository
from app.domain.dtos.user.transaction_dto import TransactionDTO
from app.domain.dtos.user.update_role_dto import UpdateRoleDTO

class UserService(IUserService):
    def __init__(self, user_repository: IUserRepository):
        self.user_repository = user_repository

    def get_all_users(self) -> Result[list[User]]:
        try:
            with get_db() as db:
                users = self.user_repository.get_all(db)
                return ok(users)

        except Exception:
            return err(status_code=ErrorType.INTERNAL_ERR, message=f'Failed to fetch all users')
    
    def get_user_by_id(self, user_id: int) -> Result[User]:
        try:
            with get_db() as db:
                user = self.user_repository.get_by_id(user_id, db)

                if not user:
                    return err(status_code=ErrorType.NOT_FOUND, message=f'User with id {user_id} not found')
                return ok(user)

        except Exception:
            return err(status_code=ErrorType.INTERNAL_ERR, message=f'Failed to retrieve user with id {user_id}')

    def get_user_by_email(self, email: str)-> Result[User]:
        try:
            with get_db() as db:
                user = self.user_repository.get_by_email(email, db)
                
                if not user:
                    return err(status_code=ErrorType.NOT_FOUND, message=f'User with email {email} not found')
                return ok(user)

        except Exception:
            return err(status_code=ErrorType.INTERNAL_ERR, message=f'Failed to retrieve user with email {email}')

    def update_user_role_by_id(self, user_id: int, data: UpdateRoleDTO)-> Result[None]:
        try:
            user_role = Role(data.role)
            with get_db_transaction() as db:
                user = self.user_repository.get_by_id(user_id, db)
                if not user:
                    return err(status_code=ErrorType.NOT_FOUND, message=f'User with id {user_id} not found')
                if user.role == Role.ADMINISTRATOR or user_role == Role.ADMINISTRATOR:
                    return err(status_code=ErrorType.FORBIDDEN, message=f'Not permitted to update the role of the user with id {user_id} to {user_role}')
                
                user.role = user_role
                return ok(None)
                
        except Exception:
            return err(status_code=ErrorType.INTERNAL_ERR, message=f'Failed to update role to {data.role} for user with id {user_id}')

    def update_user(self, user_id: int, data: UpdateUserDTO)-> Result[User]:
        try:
            with get_db_transaction() as db:
                user = self.user_repository.get_by_id(user_id, db)
                if not user:
                    return err(status_code=ErrorType.NOT_FOUND, message=f'User with id {user_id} not found')

                if hasattr(data, "email") and data.email is not None:
                    user_with_email = self.user_repository.get_by_email(data.email, db)
                    if user_id != user_with_email.user_id:
                        return err(status_code=ErrorType.FORBIDDEN, message=f'Email address already exists')

                for field, value in data.__dict__.items():
                    if value is not None:
                        setattr(user, field, value)

                return ok(user)
            
        except Exception:
            return err(status_code=ErrorType.INTERNAL_ERR, message=f'Failed to update profile for user with id {user_id}')

    def delete_user_by_id(self, user_id: int)-> Result[None]:
        try:
            with get_db_transaction() as db:
                user = self.user_repository.get_by_id(user_id, db)
                if not user:
                    return err(status_code=ErrorType.NOT_FOUND, message=f'User with id {user_id} not found')
                if user.role == Role.ADMINISTRATOR:
                    return err(status_code=ErrorType.FORBIDDEN, message=f'Not permitted to delete the user with id {user_id}')

                self.user_repository.delete_user(user, db)
                return ok(None)

        except Exception:
            return err(status_code=ErrorType.INTERNAL_ERR, message=f'Failed to delete user with id {user_id}')
        
    def deposit(self, user_id: int, data: TransactionDTO) -> Result[None]:
        try:
            with get_db_transaction() as db:
                user = self.user_repository.get_by_id(user_id, db)
                if not user:
                    return err(status_code=ErrorType.NOT_FOUND, message=f'User with id {user_id} not found')

                user.account_balance += data.amount
                return ok(None)

        except Exception:
            return err(status_code=ErrorType.INTERNAL_ERR, message=f'Failed to deposit money for user with id {user_id}')

    def withdraw(self, user_id: int, data: TransactionDTO) -> Result[None]:
        try:
            with get_db_transaction() as db:
                    user = self.user_repository.get_by_id(user_id, db)
                    if not user:
                        return err(status_code=ErrorType.NOT_FOUND, message=f'User with id {user_id} not found')
                    if user.account_balance < data.amount:
                        return err(status_code=ErrorType.BAD_REQUEST, message=f'Insufficient funds')

                    user.account_balance -= data.amount
                    return ok(None)

        except Exception:
            return err(status_code=ErrorType.INTERNAL_ERR, message=f'Failed to withdraw money for user with id {user_id}')
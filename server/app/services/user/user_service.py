import logging

from app.database import get_db, get_db_transaction

from app.domain.dtos.user.update_user_dto import UpdateUserDTO
from app.domain.services.user.iuser_service import IUserService
from app.domain.types.result import ok, err, Result
from app.domain.models.user import User
from app.domain.enums.role import Role
from app.domain.enums.error_type import ErrorType
from app.domain.dtos.user.transaction_dto import TransactionDTO
from app.domain.dtos.user.update_role_dto import UpdateRoleDTO
from app.domain.services.mail.imail_service import IMailService
from app.domain.repositories.user.iuser_repository import IUserRepository
from app.domain.repositories.redis.icache_repository import ICacheRepository

from app.services.mail.mail_formatter import MailFormatter

logger = logging.getLogger(__name__)

class UserService(IUserService):
    def __init__(self, user_repository: IUserRepository, mail_service: IMailService, cache_repository: ICacheRepository) -> None:
        self.user_repository = user_repository
        self.mail_service = mail_service
        self.cache_repository = cache_repository
        self.cache_prefix = "users:"

    def get_all_users(self) -> Result[list[User], ErrorType]:
        try:
            cache_data = self.cache_repository.get_cache(f"{self.cache_prefix}all")
            if cache_data is not None:
                return ok(cache_data)

            with get_db() as db:
                users = self.user_repository.get_all(db)
                self.cache_repository.set_cache(f"{self.cache_prefix}all", users, 60)
                return ok(users)

        except Exception as e:
            logger.error(f"Failed to fetch users: {str(e)}")
            return err(status_code=ErrorType.INTERNAL_ERR, message='Failed to fetch all users')
    
    def get_user_by_id(self, user_id: int) -> Result[User, ErrorType]:
        try:
            cache_data = self.cache_repository.get_cache(f"{self.cache_prefix}{user_id}")
            if cache_data is not None:
                return ok(cache_data)

            with get_db() as db:
                user = self.user_repository.get_by_id(user_id, db)

                if not user:
                    logger.warning(f"Failed to fetch user with id {user_id}: user not found")
                    return err(status_code=ErrorType.NOT_FOUND, message=f'User with id {user_id} not found')

                self._cache_user(user)
                return ok(user)

        except Exception as e:
            logger.error(f"Failed to fetch the user with id {user_id}: {str(e)}")
            return err(status_code=ErrorType.INTERNAL_ERR, message=f'Failed to retrieve user with id {user_id}')

    def get_user_by_email(self, email: str)-> Result[User, ErrorType]:
        try:
            cache_data = self.cache_repository.get_cache(f"{self.cache_prefix}{email}")
            if cache_data is not None:
                return ok(cache_data)

            with get_db() as db:
                user = self.user_repository.get_by_email(email, db)
                
                if not user:
                    logger.warning(f"Failed to fetch user with email {email}: user not found")
                    return err(status_code=ErrorType.NOT_FOUND, message=f'User with email {email} not found')
                
                self._cache_user(user)
                return ok(user)

        except Exception as e:
            logger.error(f"Failed to fetch user with email {email}: {str(e)}")
            return err(status_code=ErrorType.INTERNAL_ERR, message=f'Failed to retrieve user with email {email}')

    def update_user_role_by_id(self, user_id: int, data: UpdateRoleDTO)-> Result[None, ErrorType]:
        try:
            user_role = Role(data.role)
            with get_db_transaction() as db:
                user = self.user_repository.get_by_id(user_id, db)
                if not user:
                    logger.warning(f"Failed to update role of the user with id {user_id}: user not found")
                    return err(status_code=ErrorType.NOT_FOUND, message=f'User with id {user_id} not found')
                
                if user.role == Role.ADMINISTRATOR or user_role == Role.ADMINISTRATOR:
                    logger.warning(f"Failed to update role of the user with id {user_id}: forbidden")
                    return err(status_code=ErrorType.FORBIDDEN, message=f'Not permitted to update the role of the user with id {user_id} to {user_role}')
                
                previous_role = user.role
                user.role = user_role
                if previous_role == Role.USER and user_role == Role.MANAGER:
                    self.mail_service.send_async(user.email, MailFormatter.role_promotion_format(user))

                self._invalidate_user(user)
                return ok(None)
                
        except Exception as e:
            logger.error(f"Failed to update role of the user with id {user_id}: {str(e)}")
            return err(status_code=ErrorType.INTERNAL_ERR, message=f'Failed to update role to {data.role} for user with id {user_id}')

    def update_user(self, user_id: int, data: UpdateUserDTO)-> Result[User, ErrorType]:
        try:
            with get_db_transaction() as db:
                user = self.user_repository.get_by_id(user_id, db)
                if not user:
                    logger.warning(f"Failed to update user with id {user_id}: user not found")
                    return err(status_code=ErrorType.NOT_FOUND, message=f'User with id {user_id} not found')

                if hasattr(data, "email") and data.email is not None:
                    user_with_email = self.user_repository.get_by_email(data.email, db)
                    if user_with_email is not None and user_id != user_with_email.user_id:
                        logger.warning(f"Failed to update user with id {user_id}: email address already exists")
                        return err(status_code=ErrorType.CONFLICT, message=f'Email address already exists')

                old_email = user.email
                for field, value in data.__dict__.items():
                    if value is not None:
                        setattr(user, field, value)

                self._invalidate_user(user, old_email)
                return ok(user)
            
        except Exception as e:
            logger.error(f"Failed to update use with id {user_id}: {str(e)}")
            return err(status_code=ErrorType.INTERNAL_ERR, message=f'Failed to update profile for user with id {user_id}')

    def delete_user_by_id(self, user_id: int)-> Result[None, ErrorType]:
        try:
            with get_db_transaction() as db:
                user = self.user_repository.get_by_id(user_id, db)
                if not user:
                    logger.warning(f"Failed to delete user with id {user_id}: user not found")
                    return err(status_code=ErrorType.NOT_FOUND, message=f'User with id {user_id} not found')
                if user.role == Role.ADMINISTRATOR:
                    logger.warning("Failed to delete user with id {user_id}: forbidden")
                    return err(status_code=ErrorType.FORBIDDEN, message=f'Not permitted to delete the user with id {user_id}')

                self.user_repository.delete_user(user, db)
                self._invalidate_user(user)
                return ok(None)

        except Exception as e:
            logger.error(f"Failed to delete user with id {user_id}: {str(e)}")
            return err(status_code=ErrorType.INTERNAL_ERR, message=f'Failed to delete user with id {user_id}')
        
    def deposit(self, user_id: int, data: TransactionDTO) -> Result[None, ErrorType]:
        try:
            with get_db_transaction() as db:
                user = self.user_repository.get_by_id(user_id, db)
                if not user:
                    logger.warning(f"Failed to deposit money for user with id {user_id}: user not found")
                    return err(status_code=ErrorType.NOT_FOUND, message=f'User with id {user_id} not found')

                assert data.amount is not None
                user.account_balance += data.amount

                self._invalidate_user(user)
                return ok(None)

        except Exception as e:
            logger.error(f"Failed to deposit money for user with id {user_id}: {str(e)}")
            return err(status_code=ErrorType.INTERNAL_ERR, message=f'Failed to deposit money for user with id {user_id}')

    def withdraw(self, user_id: int, data: TransactionDTO) -> Result[None, ErrorType]:
        try:
            with get_db_transaction() as db:
                    user = self.user_repository.get_by_id(user_id, db)
                    if not user:
                        logger.warning(f"Failed to withdraw money for user with id {user_id}: user not found")
                        return err(status_code=ErrorType.NOT_FOUND, message=f'User with id {user_id} not found')
                    
                    assert data.amount is not None
                    if user.account_balance < data.amount:
                        logger.warning(f"Failed to withdraw money for user with id {user_id}: insufficient funds")
                        return err(status_code=ErrorType.BAD_REQUEST, message=f'Insufficient funds')

                    user.account_balance -= data.amount

                    self._invalidate_user(user)
                    return ok(None)

        except Exception as e:
            logger.error(f"Failed to withdraw money for user with id {user_id}: {str(e)}")
            return err(status_code=ErrorType.INTERNAL_ERR, message=f'Failed to withdraw money for user with id {user_id}')
        
    def _cache_user(self, user: User) -> None:
            self.cache_repository.set_cache(f"{self.cache_prefix}{user.user_id}", user, 300)
            self.cache_repository.set_cache(f"{self.cache_prefix}{user.email}", user, 300)

    def _invalidate_user(self, user: User, old_email: str | None = None) -> None:
        self.cache_repository.delete_cache(f"{self.cache_prefix}{user.user_id}")
        self.cache_repository.delete_cache(f"{self.cache_prefix}{user.email}")
        
        if old_email and old_email != user.email:
            self.cache_repository.delete_cache(f"{self.cache_prefix}{old_email}")

        self.cache_repository.delete_cache(f"{self.cache_prefix}all")

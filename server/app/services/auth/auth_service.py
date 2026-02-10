
from dataclasses import asdict
import logging
from werkzeug.security import generate_password_hash, check_password_hash

from app.database import get_db, get_db_transaction

from app.domain.models.user import User
from app.domain.dtos.auth.login_user_dto import LoginUserDTO
from app.domain.dtos.auth.register_user_dto import RegisterUserDTO
from app.domain.enums.role import Role
from app.domain.services.auth.iauth_service import IAuthService
from app.domain.types.result import Result, err, ok

from app.repositories.user.user_repository import IUserRepository
from app.repositories.redis.blacklist_repository import IBlacklistRepository
from app.repositories.redis.blocklist_repository import IBlocklistRepository

from app.services.user.user_service import ErrorType

logger = logging.getLogger(__name__)

class AuthService(IAuthService):
    def __init__(self, user_repository: IUserRepository, blacklist_repository: IBlacklistRepository, blocklist_repository: IBlocklistRepository) -> None:
        self.user_repository = user_repository
        self.blacklist_repository = blacklist_repository
        self.blocklist_repository = blocklist_repository
    
    def login(self, login_dto: LoginUserDTO, ip_address: str) -> Result[User, ErrorType]:
        try:
            with get_db() as db:
                if(self.blocklist_repository.is_blocked(ip_address)):
                    logger.warning(f"IP address {ip_address} temporarily blocked due to multiple invalid login attempts")
                    return err(ErrorType.TOO_MANY_REQUESTS, 'Too many requests, try logging in later')
                
                assert login_dto.email is not None and login_dto.password is not None
                user = self.user_repository.get_by_email(login_dto.email, db)
                if not user or not check_password_hash(user.password, login_dto.password):
                    self.blocklist_repository.add_attempt_to_blocklist(ip_address)
                    logger.warning(f"Login failed: invalid credentials")
                    return err(ErrorType.UNAUTHORIZED, 'Invalid credentials')
                
                return ok(user)
        except Exception as e:
            logger.error(f'Login failed: {str(e)}')
            return err(ErrorType.INTERNAL_ERR, 'Internal server error - failed to log in')
    
    def register(self, register_dto: RegisterUserDTO) -> Result[User, ErrorType]:
        try:
            with get_db_transaction() as db:
                assert register_dto.email is not None and register_dto.password is not None
                if self.user_repository.get_by_email(register_dto.email, db):
                    logger.warning("Registration failed - email is already in use")
                    return err(ErrorType.CONFLICT, 'Email already registered')
                
                password = generate_password_hash(register_dto.password)
                user_data = asdict(register_dto)
                user_data["password"] = password
                user_data["role"] = Role.USER

                user = User(**user_data)
                saved_user = self.user_repository.create(user, db)
                return ok(saved_user)
        except Exception as e:
            logger.error(f"Registration failed: {str(e)}")
            return err(ErrorType.INTERNAL_ERR, 'Internal server error - failed to register')
        
    def logout(self, jwt_token: str) -> Result[None, ErrorType]:
        try:
            self.blacklist_repository.add_to_blacklist(jwt_token)
            return ok(None)
        except Exception as e:
            logger.error(f"Logging out failed: {str(e)}")
            return err(ErrorType.INTERNAL_ERR, "Internal server error - failed to log out")
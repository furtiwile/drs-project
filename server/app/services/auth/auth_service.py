
from dataclasses import asdict
from app.domain.models.user import User
from werkzeug.security import generate_password_hash, check_password_hash
from app.database import get_db, get_db_transaction
from app.domain.dtos.auth.login_user_dto import LoginUserDTO
from app.domain.dtos.auth.register_user_dto import RegisterUserDTO
from app.domain.enums.role import Role
from app.domain.services.auth.iauth_service import IAuthService
from app.domain.types.result import Result, err, ok
from app.repositories.user.user_repository import IUserRepository
from app.services.user.user_service import ErrorType
from app.repositories.redis.blacklist_repository import IBlacklistRepository
from app.repositories.redis.blocklist_repository import IBlocklistRepository


class AuthService(IAuthService):
    def __init__(self, user_repository: IUserRepository, blacklist_repository: IBlacklistRepository, blocklist_repository: IBlocklistRepository):
        self.user_repository = user_repository
        self.blacklist_repository = blacklist_repository
        self.blocklist_repository = blocklist_repository
    
    def login(self, login_dto: LoginUserDTO, ip_address: str) -> Result[User]:
        try:
            with get_db() as db:
                if(self.blocklist_repository.is_blocked(ip_address)):
                    return err(ErrorType.TOO_MANY_REQUESTS, 'Too many requests, try logging in later')
                
                user = self.user_repository.get_by_email(login_dto.email, db)
                if not user or not check_password_hash(user.password, login_dto.password):
                    self.blocklist_repository.add_attempt_to_blocklist(ip_address)
                    return err(ErrorType.UNAUTHORIZED, 'Invalid credentials')
                
                return ok(user)
        except Exception:
            return err(ErrorType.INTERNAL_ERR, 'Internal server error - failed to log in')
    
    def register(self, register_dto: RegisterUserDTO) -> Result[User]:
        try:
            with get_db_transaction() as db:
                if self.user_repository.get_by_email(register_dto.email, db):
                    return err(ErrorType.CONFLICT, 'Email already registered')
                
                password = generate_password_hash(register_dto.password)
                user_data = asdict(register_dto)
                user_data["password"] = password
                user_data["role"] = Role.USER

                user = User(**user_data)
                saved_user = self.user_repository.create(user, db)
                return ok(saved_user)
        except Exception:
            return err(ErrorType.INTERNAL_ERR, 'Internal server error - failed to register')
        
    def logout(self, jwt_token: str) -> Result[None]:
        try:
            self.blacklist_repository.add_to_blacklist(jwt_token)
            return ok(None)
        except Exception:
            return err(ErrorType.INTERNAL_ERR, "Internal server error - failed to log out")
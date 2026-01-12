
from dataclasses import asdict
from app.domain.models.User import User
from werkzeug.security import generate_password_hash, check_password_hash
from app.database import get_db, get_db_transaction
from app.domain.dtos.auth.login_user_dto import LoginUserDTO
from app.domain.dtos.auth.register_user_dto import RegisterUserDTO
from app.domain.enums.Role import Role
from app.domain.services.iauth_service import IAuthService
from app.domain.types.Result import Result, err, ok
from app.repositories.user_repository import IUserRepository
from app.services.user_service import ErrorType


class AuthService(IAuthService):
    def __init__(self, user_repository: IUserRepository):
        self.user_repository = user_repository
    
    def login(self, login_dto: LoginUserDTO) -> Result[User]:
        try:
            with get_db() as db:
                user = self.user_repository.get_by_email(login_dto.email, db)
                
                if not user or not check_password_hash(user.password, login_dto.password):
                    return err(ErrorType.UNAUTHORIZED, 'Invalid credentials')
                
                return ok(user)
        except:
            return err(ErrorType.INTERNAL_ERR, 'Internal server error')
    
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
        except:
            return err(ErrorType.INTERNAL_ERR, 'Internal server error')
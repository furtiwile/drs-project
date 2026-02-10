from abc import abstractmethod

from app.domain.models.user import User
from app.domain.types.result import Result
from app.domain.dtos.auth.login_user_dto import LoginUserDTO
from app.domain.dtos.auth.register_user_dto import RegisterUserDTO
from app.domain.enums.error_type import ErrorType

class IAuthService:
    @abstractmethod
    def login(self, login_dto: LoginUserDTO, ip_address: str) -> Result[User, ErrorType]:
        pass
    
    @abstractmethod
    def register(self, register_dto: RegisterUserDTO) -> Result[User, ErrorType]:
        pass

    @abstractmethod
    def logout(self, jwt_token: str) -> Result[None, ErrorType]:
        pass
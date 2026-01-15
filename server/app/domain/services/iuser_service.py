from abc import abstractmethod
from app.domain.dtos.user.update_user_dto import UpdateUserDTO
from app.domain.enums.Role import Role
from app.domain.models.User import User
from app.domain.types.Result import Result

class IUserService:
    @abstractmethod
    def get_all_users(self) -> Result[list[User]]:
        pass

    @abstractmethod
    def get_user_by_id(self, user_id: int) -> Result[User]:
        pass

    @abstractmethod
    def get_user_by_email(self, email: str)-> Result[User]:
        pass

    @abstractmethod
    def update_user_role_by_id(self, user_id: int, user_role: Role)-> Result[None]:
        pass

    @abstractmethod
    def update_user(self, user_id, data: UpdateUserDTO)-> Result[User]:
        pass

    @abstractmethod
    def delete_user_by_id(self, user_id: int)-> Result[None]:
        pass
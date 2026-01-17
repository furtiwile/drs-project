from abc import abstractmethod
from app.domain.dtos.user.update_user_dto import UpdateUserDTO
from app.domain.models.user import User
from app.domain.types.result import Result
from app.domain.dtos.user.transaction_dto import TransactionDTO
from app.domain.dtos.user.update_role_dto import UpdateRoleDTO

class IUserService:
    @abstractmethod
    def get_all_users(self) -> Result[list[User]]:
        pass

    @abstractmethod
    def get_user_by_id(self, user_id: int) -> Result[User]:
        pass

    @abstractmethod
    def get_user_by_email(self, email: str) -> Result[User]:
        pass

    @abstractmethod
    def update_user_role_by_id(self, user_id: int, data: UpdateRoleDTO) -> Result[None]:
        pass

    @abstractmethod
    def update_user(self, user_id, data: UpdateUserDTO) -> Result[User]:
        pass

    @abstractmethod
    def delete_user_by_id(self, user_id: int) -> Result[None]:
        pass

    @abstractmethod
    def deposit(self, user_id: int, data: TransactionDTO) -> Result[None]:
        pass

    @abstractmethod
    def withdraw(self, user_id: int, data: TransactionDTO) -> Result[None]:
        pass
from dataclasses import asdict, dataclass
from datetime import date

from app.domain.enums.gender import Gender
from app.domain.enums.role import Role
from app.domain.models.user import User

@dataclass
class UserDTO:
    user_id: int
    first_name: str
    last_name: str
    email: str
    birth_date: date
    gender: Gender
    country: str
    city: str
    street: str
    house_number: int
    account_balance: float
    role: Role
    profile_picture: str

    @classmethod
    def from_model(cls, user: User):
        return cls(
            user_id=user.user_id,
            first_name=user.first_name,
            last_name=user.last_name,
            email=user.email,
            birth_date=user.birth_date,
            gender=user.gender,
            country=user.country,
            city=user.city,
            street=user.street,
            house_number=user.house_number,
            account_balance=user.account_balance,
            role=user.role,
            profile_picture=user.profile_picture
        )

    def to_dict(self) -> dict:
        return {
            **asdict(self),
            "birth_date": self.birth_date.isoformat(),
            "gender": self.gender.value,
            "role": self.role.value,
        }
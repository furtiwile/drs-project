from dataclasses import dataclass
from datetime import date
from app.domain.enums.Gender import Gender
from app.domain.enums.Role import Role

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
    profile_picture

    @classmethod
    def from_model(cls, user):
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

    @classmethod
    def to_dict(self) -> dict:
        return {
            'user_id': self.user_id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'user_id': self.user_id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email,
            'birth_date': self.birth_date.isoformat(),
            'gender': self.gender.value,
            'country': self.country,
            'city': self.city,
            'street': self.street,
            'house_number': self.house_number,
            'account_balance': self.account_balance,
            'role': self.role.value,
            'profile_picture': self.profile_picture
        }
from dataclasses import dataclass
from datetime import date, datetime
from typing import Any, Self

from app.domain.enums.gender import Gender

@dataclass
class CreateUserDTO:
    first_name: str | None
    last_name: str | None
    email: str | None
    password: str | None
    birth_date: date | None
    gender: Gender | None
    country: str | None
    city: str | None
    street: str | None
    house_number: int | None
    profile_picture: str | None

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Self:
        if isinstance(data.get('birth_date'), str):
            data['birth_date'] = datetime.strptime(data['birth_date'], '%Y-%m-%d').date()
        
        return cls(
            first_name=data.get('first_name'),
            last_name=data.get('last_name'),
            email=data.get('email'),
            password=data.get('password'),
            birth_date=data.get('birth_date'),
            gender=data.get('gender'),
            country=data.get('country'),
            city=data.get('city'),
            street=data.get('street'),
            house_number=data.get('house_number'),
            profile_picture=data.get('profile_picture')
        )
from dataclasses import dataclass
from typing import Any, Self
from datetime import date, datetime

from app.domain.enums.gender import Gender

@dataclass
class UpdateUserDTO:
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
        birth_date = data.get('birth_date')
        if birth_date and isinstance(birth_date, str):
            birth_date = datetime.strptime(birth_date, '%Y-%m-%d').date()
        
        gender = None
        if 'gender' in data and data['gender']:
            gender = Gender[data['gender'].upper()]
        
        return cls(
            first_name=data.get('first_name'),
            last_name=data.get('last_name'),
            email=data.get('email'),
            password=data.get('password'),
            birth_date=birth_date,
            gender=gender,
            country=data.get('country'),
            city=data.get('city'),
            street=data.get('street'),
            house_number=data.get('house_number'),
            profile_picture=data.get('profile_picture')
        )
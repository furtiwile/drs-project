from dataclasses import dataclass
from datetime import date, datetime
from typing import Optional
from app.domain.enums.Gender import Gender


@dataclass
class RegisterUserDTO:
    first_name: Optional[str]
    last_name: Optional[str]
    email: Optional[str]
    password: Optional[str]
    birth_date: Optional[date]
    gender: Optional[Gender]
    country: Optional[str]
    city: Optional[str]
    street: Optional[str]
    house_number: Optional[int]
    profile_picture: Optional[str]

    @classmethod
    def from_dict(cls, data: dict):
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
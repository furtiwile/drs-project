from dataclasses import dataclass
from datetime import date
from typing import Optional
from app.domain.enums.gender import Gender

@dataclass
class CreateUserDTO:
    first_name: str
    last_name: str
    email: str
    password: str
    birth_date: date
    gender: Gender
    country: str
    city: str
    street: str
    house_number: int
    profile_picture: Optional[str]

    @classmethod
    def from_dict(cls, data: dict):
        from datetime import datetime
        
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
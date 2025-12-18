from dataclasses import dataclass
from typing import Optional
from datetime import date
from app.domain.enums.Gender import Gender
from app.domain.enums.Role import Role

@dataclass
class UpdateUserDTO:
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None
    birth_date: Optional[date] = None
    gender: Optional[Gender] = None
    country: Optional[str] = None
    city: Optional[str] = None
    street: Optional[str] = None
    house_number: Optional[int] = None
    role: Optional[Role] = None
    profile_picture: Optional[str] = None
    
    @classmethod
    def from_dict(cls, data: dict):
        birth_date = data.get('birth_date')
        if birth_date and isinstance(birth_date, str):
            birth_date = datetime.strptime(birth_date, '%Y-%m-%d').date()
        
        gender = None
        if 'gender' in data and data['gender']:
            gender = Gender[data['gender'].upper()]
        
        role = None
        if 'role' in data and data['role']:
            role = Role[data['role'].upper()]
        
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
            role=role,
            profile_picture=data.get('profile_picture')
        )
    
    def to_dict(self, exclude_none=True):
        data = {
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email,
            'password': self.password,
            'birth_date': self.birth_date.isoformat() if self.birth_date else None,
            'gender': self.gender.value if self.gender else None,
            'country': self.country,
            'city': self.city,
            'street': self.street,
            'house_number': self.house_number,
            'role': self.role.value if self.role else None,
            'profile_picture': self.profile_picture
        }
        
        if exclude_none:
            return {k: v for k, v in data.items() if v is not None}
        
        return data
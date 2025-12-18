from dataclasses import dataclass
from datetime import date
from app.domain.enums.Gender import Gender
from app.domain.enums.Role import Role

@dataclass
class CreateUserDTO:
    first_name: str
    last_name: str
    email: str
    birth_date: date
    gender: Gender
    country: str
    city: str
    street: str
    house_number: int
    profile_picture: str

    @classmethod
    def from_dict(cls, data: dict):
        from datetime import datetime
        
        if isinstance(data.get('birth_date'), str):
            data['birth_date'] = datetime.strptime(data['birth_date'], '%Y-%m-%d').date()
        
        return cls(
            first_name=data['first_name'],
            last_name=data['last_name'],
            email=data['email'],
            password=data['password'],
            birth_date=data['birth_date'],
            gender=data['gender'],
            country=data['country'],
            city=data['city'],
            street=data['street'],
            house_number=data['house_number'],
            profile_picture=data['profile_picture']
        )
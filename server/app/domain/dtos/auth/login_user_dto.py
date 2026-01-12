from dataclasses import dataclass
from typing import Optional

@dataclass
class LoginUserDTO:
    email: Optional[str]
    password: Optional[str]

    @classmethod
    def from_dict(cls, data: dict) -> "LoginUserDTO":
        return cls(
            email=data.get("email"),
            password=data.get('password')
        )
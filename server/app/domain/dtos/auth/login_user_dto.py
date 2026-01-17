from dataclasses import dataclass
from typing import Self

@dataclass
class LoginUserDTO:
    email: str | None
    password: str | None

    @classmethod
    def from_dict(cls, data: dict[str, str | None]) -> Self:
        return cls(
            email=data.get("email"),
            password=data.get('password')
        )
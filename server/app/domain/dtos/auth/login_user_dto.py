from dataclasses import dataclass
from typing import Any, Self

@dataclass
class LoginUserDTO:
    email: str | None
    password: str | None

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Self:
        return cls(
            email=data.get("email"),
            password=data.get('password')
        )
from dataclasses import dataclass
from typing import Self

@dataclass
class UpdateRoleDTO:
    role: str | None

    @classmethod
    def from_dict(cls, data: dict[str, str | None]) -> Self:
        return cls(
            role=data.get('role')
        )
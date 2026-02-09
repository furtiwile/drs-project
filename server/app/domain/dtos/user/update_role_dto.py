from dataclasses import dataclass
from typing import Any, Self

@dataclass
class UpdateRoleDTO:
    role: str | None

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Self:
        return cls(
            role=data.get('role')
        )
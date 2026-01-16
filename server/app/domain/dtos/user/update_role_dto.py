from dataclasses import dataclass
from typing import Optional

@dataclass
class UpdateRoleDTO:
    role: Optional[str]

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            role=data.get('role')
        )
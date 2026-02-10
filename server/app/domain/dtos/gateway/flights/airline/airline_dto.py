from dataclasses import asdict, dataclass
from datetime import datetime
from typing import Any, Self

@dataclass
class AirlineDTO:
    id: int | None
    name: str | None
    created_at: datetime | None

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Self:
        return cls(
            id=data.get('id'),
            name=data.get('name'),
            created_at=data.get('created_at')
        )
    
    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

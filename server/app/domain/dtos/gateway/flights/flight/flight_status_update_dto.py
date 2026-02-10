from dataclasses import asdict, dataclass
from typing import Any, Self

@dataclass
class FlightStatusUpdateDTO:
    status: str | None
    rejection_reason: str | None

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Self:
        return cls(
            status=data.get('status'),
            rejection_reason=data.get('rejection_reason')
        )
    
    def to_dict(self) -> dict[str, Any]:
        return asdict(self)
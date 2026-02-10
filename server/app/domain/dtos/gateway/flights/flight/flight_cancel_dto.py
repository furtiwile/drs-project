from dataclasses import asdict, dataclass
from typing import Any, Self

@dataclass
class FlightCancelDTO:
    cancellation_reason: str | None

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Self:
        return cls(
            cancellation_reason=data.get('cancellation_reason')
        )
    
    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

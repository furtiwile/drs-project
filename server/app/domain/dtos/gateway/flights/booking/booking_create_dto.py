from dataclasses import asdict, dataclass
from typing import Any, Self

@dataclass
class BookingCreateDTO:
    flight_id: int | None

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Self:
        return cls(
            flight_id=data.get('flight_id')
        )
    
    def to_dict(self) -> dict[str, Any]:
        return asdict(self)
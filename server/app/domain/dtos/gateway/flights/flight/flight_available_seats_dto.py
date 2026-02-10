from dataclasses import asdict, dataclass
from typing import Any, Self

@dataclass
class FlightAvailableSeatsDTO:
    flight_id: int | None
    available_seats: int | None

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Self:
        return cls(
            flight_id=data.get('flight_id'),
            available_seats=data.get('available_seats')
        )
    
    def to_dict(self) -> dict[str, Any]:
        return asdict(self)
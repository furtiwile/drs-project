from typing import List
from dataclasses import dataclass
from typing import Any, Self

from app.domain.dtos.gateway.flights.flight.flight_dto import FlightDTO

@dataclass
class FlightCancelledDTO:
    flight: FlightDTO | None
    affected_user_ids: List[int] | None

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Self:
        return cls(
            flight=FlightDTO.from_dict(data['flight']) if data.get('flight') else None,
            affected_user_ids=data.get('affected_user_ids')
        )
    
    def to_dict(self) -> dict[str, Any]:
        return { 
            "flight": self.flight.to_dict() if self.flight is not None else None,
            "affected_user_ids": self.affected_user_ids
        }

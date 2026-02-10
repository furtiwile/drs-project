from dataclasses import dataclass
from datetime import datetime
from typing import Any, Self

from app.domain.dtos.gateway.flights.flight.flight_dto import FlightDTO

@dataclass
class RatingDTO:
    id: int | None
    user_id: int | None
    flight_id: int | None
    flight: FlightDTO | None
    rating: int | None
    created_at: datetime | None

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Self:
        return cls(
            id=data.get("id"),
            user_id=data.get("user_id"),
            flight_id=data.get("flight_id"),
            flight=(
                FlightDTO.from_dict(data["flight"])
                if data.get("flight")
                else None
            ),
            rating=data.get("rating"),
            created_at=(
                datetime.fromisoformat(data["created_at"])
                if data.get("created_at")
                else None
            ),
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "user_id": self.user_id,
            "flight_id": self.flight_id,
            "flight": (
                self.flight.to_dict()
                if self.flight
                else None
            ),
            "rating": self.rating,
            "created_at": (
                self.created_at.isoformat()
                if self.created_at
                else None
            ),
        }
from dataclasses import dataclass
from datetime import datetime
from typing import Any, Self

@dataclass
class FlightRemainingTimeDTO:
    flight_id: int | None
    remaining_seconds: int | None
    remaining_minutes: int | None
    arrival_time: datetime | None
    status: str | None

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Self:
        return cls(
            flight_id=data.get("flight_id"),
            remaining_seconds=data.get("remaining_seconds"),
            remaining_minutes=data.get("remaining_minutes"),
            arrival_time=(
                datetime.fromisoformat(data["arrival_time"])
                if data.get("arrival_time")
                else None
            ),
            status=data.get("status"),
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "flight_id": self.flight_id,
            "remaining_seconds": self.remaining_seconds,
            "remaining_minutes": self.remaining_minutes,
            "arrival_time": (
                self.arrival_time.isoformat()
                if self.arrival_time
                else None
            ),
            "status": self.status,
        }
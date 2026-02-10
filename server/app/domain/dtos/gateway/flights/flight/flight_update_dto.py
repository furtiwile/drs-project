from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from typing import Any, Self


@dataclass
class FlightUpdateDTO:
    flight_name: str | None
    airline_id: int | None
    flight_distance_km: int | None
    flight_duration: int | None
    departure_time: datetime | None
    departure_airport_id: int | None
    arrival_airport_id: int | None
    price: Decimal | None
    total_seats: int | None
    rejection_reason: str | None
    approved_by: int | None
    actual_start_time: datetime | None

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Self:
        return cls(
            flight_name=data.get("flight_name"),
            airline_id=data.get("airline_id"),
            flight_distance_km=data.get("flight_distance_km"),
            flight_duration=data.get("flight_duration"),
            departure_time=(
                datetime.fromisoformat(data["departure_time"])
                if data.get("departure_time")
                else None
            ),
            departure_airport_id=data.get("departure_airport_id"),
            arrival_airport_id=data.get("arrival_airport_id"),
            price=(
                Decimal(data["price"])
                if data.get("price") is not None
                else None
            ),
            total_seats=data.get("total_seats"),
            rejection_reason=data.get("rejection_reason"),
            approved_by=data.get("approved_by"),
            actual_start_time=(
                datetime.fromisoformat(data["actual_start_time"])
                if data.get("actual_start_time")
                else None
            ),
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "flight_name": self.flight_name,
            "airline_id": self.airline_id,
            "flight_distance_km": self.flight_distance_km,
            "flight_duration": self.flight_duration,
            "departure_time": (
                self.departure_time.isoformat()
                if self.departure_time
                else None
            ),
            "departure_airport_id": self.departure_airport_id,
            "arrival_airport_id": self.arrival_airport_id,
            "price": (
                str(self.price)
                if self.price is not None
                else None
            ),
            "total_seats": self.total_seats,
            "rejection_reason": self.rejection_reason,
            "approved_by": self.approved_by,
            "actual_start_time": (
                self.actual_start_time.isoformat()
                if self.actual_start_time
                else None
            ),
        }
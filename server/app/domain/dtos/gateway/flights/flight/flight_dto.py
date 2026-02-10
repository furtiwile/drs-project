from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from typing import Any

from app.domain.dtos.gateway.flights.airline.airline_dto import AirlineDTO
from app.domain.dtos.gateway.flights.airport.airport_dto import AirportDTO

@dataclass
class FlightDTO:
    flight_id: int | None
    flight_name: str | None
    airline_id: int | None
    airline: AirlineDTO | None
    flight_distance_km: int | None
    flight_duration: str | None
    departure_time: datetime | None
    arrival_time: datetime | None
    departure_airport_id: int | None
    departure_airport: AirportDTO | None
    arrival_airport_id: int | None
    arrival_airport: AirportDTO | None
    created_by: int | None
    price: Decimal | None
    total_seats: int | None
    available_seats: int | None
    status: str | None
    rejection_reason: str | None
    approved_by: int | None
    actual_start_time: datetime | None
    created_at: datetime | None
    updated_at: datetime | None

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "FlightDTO":
        return cls(
            flight_id=data.get("flight_id"),
            flight_name=data.get("flight_name"),
            airline_id=data.get("airline_id"),
            airline=(
                AirlineDTO.from_dict(data["airline"])
                if data.get("airline")
                else None
            ),
            flight_distance_km=data.get("flight_distance_km"),
            flight_duration=data.get("flight_duration"),
            departure_time=(
                datetime.fromisoformat(data["departure_time"])
                if data.get("departure_time")
                else None
            ),
            arrival_time=(
                datetime.fromisoformat(data["arrival_time"])
                if data.get("arrival_time")
                else None
            ),
            departure_airport_id=data.get("departure_airport_id"),
            departure_airport=(
                AirportDTO.from_dict(data["departure_airport"])
                if data.get("departure_airport")
                else None
            ),
            arrival_airport_id=data.get("arrival_airport_id"),
            arrival_airport=(
                AirportDTO.from_dict(data["arrival_airport"])
                if data.get("arrival_airport")
                else None
            ),
            created_by=data.get("created_by"),
            price=(
                Decimal(data["price"])
                if data.get("price") is not None
                else None
            ),
            total_seats=data.get("total_seats"),
            available_seats=data.get("available_seats"),
            status=data.get("status"),
            rejection_reason=data.get("rejection_reason"),
            approved_by=data.get("approved_by"),
            actual_start_time=(
                datetime.fromisoformat(data["actual_start_time"])
                if data.get("actual_start_time")
                else None
            ),
            created_at=(
                datetime.fromisoformat(data["created_at"])
                if data.get("created_at")
                else None
            ),
            updated_at=(
                datetime.fromisoformat(data["updated_at"])
                if data.get("updated_at")
                else None
            ),
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "flight_id": self.flight_id,
            "flight_name": self.flight_name,
            "airline_id": self.airline_id,
            "airline": (
                self.airline.to_dict()
                if self.airline
                else None
            ),
            "flight_distance_km": self.flight_distance_km,
            "flight_duration": self.flight_duration,
            "departure_time": (
                self.departure_time.isoformat()
                if self.departure_time
                else None
            ),
            "arrival_time": (
                self.arrival_time.isoformat()
                if self.arrival_time
                else None
            ),
            "departure_airport_id": self.departure_airport_id,
            "departure_airport": (
                self.departure_airport.to_dict()
                if self.departure_airport
                else None
            ),
            "arrival_airport_id": self.arrival_airport_id,
            "arrival_airport": (
                self.arrival_airport.to_dict()
                if self.arrival_airport
                else None
            ),
            "created_by": self.created_by,
            "price": (
                str(self.price)
                if self.price is not None
                else None
            ),
            "total_seats": self.total_seats,
            "available_seats": self.available_seats,
            "status": self.status,
            "rejection_reason": self.rejection_reason,
            "approved_by": self.approved_by,
            "actual_start_time": (
                self.actual_start_time.isoformat()
                if self.actual_start_time
                else None
            ),
            "created_at": (
                self.created_at.isoformat()
                if self.created_at
                else None
            ),
            "updated_at": (
                self.updated_at.isoformat()
                if self.updated_at
                else None
            ),
        }
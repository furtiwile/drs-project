from marshmallow import Schema, fields, validate
from dataclasses import dataclass
from datetime import datetime
from typing import Any, Optional, Self


@dataclass
class BookingCreateDTO:
    """Data transfer object for validated booking creation data."""
    flight_id: int


class BookingCreateValidationSchema(Schema):
    """Validation schema for booking creation data"""
    flight_id = fields.Int(required=True, validate=validate.Range(min=1))


@dataclass
class BookingUpdateDTO:
    """Data transfer object for validated booking update data."""
    rating: int


class BookingUpdateValidationSchema(Schema):
    """Validation schema for booking update data"""
    rating = fields.Int(required=True, validate=validate.Range(min=1, max=5))


class BookingResponseDTO(Schema):
    """DTO for booking response"""
    id = fields.Int()
    user_id = fields.Int()
    flight_id = fields.Int()
    flight = fields.Nested('FlightResponseDTO')
    purchased_at = fields.DateTime()


class BookingWithUserDTO(Schema):
    """DTO for booking with user information (for admin view)"""
    id = fields.Int()
    user_id = fields.Int()
    user_name = fields.Str()
    user_email = fields.Str()
    flight_id = fields.Int()
    flight_name = fields.Str()
    purchased_at = fields.DateTime()


@dataclass
class BookingCreateDTOReturn:
    """DTO for returning booking creation data."""
    flight_id: int
    user_id: int
    purchased_at: datetime
    flight_price: float


@dataclass
class BookingDTO:
    """Data transfer object for booking response."""
    id: Optional[int] = None
    user_id: Optional[int] = None
    flight_id: Optional[int] = None
    flight: Optional[Any] = None  # FlightDTO
    created_at: Optional[datetime] = None

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Self:
        """Create BookingDTO from dictionary."""
        return cls(
            id=data.get("id"),
            user_id=data.get("user_id"),
            flight_id=data.get("flight_id"),
            flight=data.get("flight"),
            created_at=data.get("created_at"),
        )

    @classmethod
    def from_model(cls, booking: Any) -> Self:
        """Create BookingDTO from Booking model."""
        flight_dto = None
        if booking.flight:
            # Convert flight model to dict for now, can be enhanced with FlightDTO
            flight_dto = {
                'flight_id': booking.flight.flight_id,
                'flight_name': booking.flight.flight_name,
                'airline_id': booking.flight.airline_id,
                'departure_time': booking.flight.departure_time,
                'arrival_time': booking.flight.arrival_time,
                'price': float(booking.flight.price),
                'status': booking.flight.status.value if hasattr(booking.flight.status, 'value') else str(booking.flight.status),
            }
        
        return cls(
            id=booking.id,
            user_id=booking.user_id,
            flight_id=booking.flight_id,
            flight=flight_dto,
            created_at=booking.purchased_at,
        )

    def to_dict(self) -> dict[str, Any]:
        """Convert BookingDTO to dictionary."""
        return {
            "id": self.id,
            "user_id": self.user_id,
            "flight_id": self.flight_id,
            "flight": self.flight,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }

from marshmallow import Schema, fields, validate
from dataclasses import dataclass
from datetime import datetime


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

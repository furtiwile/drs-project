from marshmallow import Schema, fields, validate
from dataclasses import dataclass


@dataclass
class RatingCreateDTO:
    """Data transfer object for validated rating creation data."""
    user_id: int
    flight_id: int
    rating: int


@dataclass
class RatingUpdateDTO:
    """Data transfer object for validated rating update data."""
    rating: int


class RatingCreateValidationSchema(Schema):
    """Validation schema for rating creation data"""
    flight_id = fields.Int(required=True, validate=validate.Range(min=1))
    rating = fields.Int(required=True, validate=validate.Range(min=1, max=5))


class RatingUpdateValidationSchema(Schema):
    """Validation schema for rating update data"""
    rating = fields.Int(required=True, validate=validate.Range(min=1, max=5))
    user_id = fields.Int(validate=validate.Range(min=1), data_key='user-id')


class RatingResponseDTO(Schema):
    """DTO for rating response"""
    id = fields.Int()
    user_id = fields.Int()
    flight_id = fields.Int()
    flight = fields.Nested('FlightResponseDTO')
    rating = fields.Int()
    created_at = fields.DateTime()


class RatingWithUserDTO(Schema):
    """DTO for rating with user information (for admin view)"""
    id = fields.Int()
    user_id = fields.Int()
    user_name = fields.Str()
    user_email = fields.Str()
    flight_id = fields.Int()
    flight_name = fields.Str()
    rating = fields.Int()
    created_at = fields.DateTime()
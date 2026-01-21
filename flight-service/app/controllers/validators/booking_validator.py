from marshmallow import Schema, fields, validate
from ...domain.dtos.booking_dto import BookingCreateDTO, BookingUpdateDTO
from typing import Dict, Any, cast


class BookingCreateValidationSchema(Schema):
    """Validation schema for booking creation data"""
    flight_id = fields.Int(required=True, validate=validate.Range(min=1))


class BookingUpdateValidationSchema(Schema):
    """Validation schema for booking update data"""
    rating = fields.Int(required=True, validate=validate.Range(min=1, max=5))


def validate_create_booking_data(data: Dict[str, Any]) -> BookingCreateDTO:
    """Validate and load booking creation data into a data object."""
    schema = BookingCreateValidationSchema()
    errors = schema.validate(data)
    if errors:
        raise ValueError(errors)
    
    validated_dict: Dict[str, Any] = cast(Dict[str, Any], schema.load(data))
    return BookingCreateDTO(
        flight_id=validated_dict['flight_id']
    )


def validate_update_booking_data(data: Dict[str, Any]) -> BookingUpdateDTO:
    """Validate and load booking update data into a data object."""
    schema = BookingUpdateValidationSchema()
    errors = schema.validate(data)
    if errors:
        raise ValueError(errors)
    
    validated_dict: Dict[str, Any] = cast(Dict[str, Any], schema.load(data))
    return BookingUpdateDTO(
        rating=validated_dict['rating']
    )
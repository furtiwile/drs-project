from marshmallow import Schema, fields, validate, validates, ValidationError, validates_schema
from ...domain.dtos.flight_dto import FlightCreateDTO, FlightUpdateDTO, FlightStatusUpdateDTO
from typing import Dict, Any, cast, Optional
from datetime import datetime, timezone
from ...domain.enums.flight_status import FlightStatus

class FlightCreateValidationSchema(Schema):
    """Validation schema for flight creation data"""
    flight_name = fields.Str(required=True, validate=validate.Length(min=3, max=255))
    airline_id = fields.Int(required=True, validate=validate.Range(min=1))
    flight_distance_km = fields.Int(required=True, validate=validate.Range(min=1)) # in kilometers
    flight_duration = fields.Int(required=True, validate=validate.Range(min=1))  # in minutes
    departure_time = fields.DateTime(required=True)
    departure_airport_id = fields.Int(required=True, validate=validate.Range(min=1))
    arrival_airport_id = fields.Int(required=True, validate=validate.Range(min=1))
    price = fields.Decimal(required=True, validate=validate.Range(min=0.01))
    total_seats = fields.Int(required=True, validate=validate.Range(min=1))

    @validates('departure_time')
    def validate_departure_time(self, value):
        if value < datetime.now(timezone.utc):
            raise ValidationError('Departure time must be in the future')

    @validates_schema
    def validate_airports_different(self, data, **kwargs):
        if data.get('departure_airport_id') == data.get('arrival_airport_id'):
            raise ValidationError('Departure and arrival airports must be different')


def validate_create_flight_data(data: Dict[str, Any]) -> FlightCreateDTO:
    """Validate and load flight creation data into a data object."""
    schema = FlightCreateValidationSchema()
    errors = schema.validate(data)
    if errors:
        raise ValueError(errors)
    
    validated_dict: Dict[str, Any] = cast(Dict[str, Any], schema.load(data))
    return FlightCreateDTO(**validated_dict)


class FlightUpdateValidationSchema(Schema):
    """Validation schema for flight update data"""
    flight_name = fields.Str(required=False, validate=validate.Length(min=3, max=255))
    airline_id = fields.Int(required=False, validate=validate.Range(min=1))
    flight_distance_km = fields.Int(required=False, validate=validate.Range(min=1))
    flight_duration = fields.Int(required=False, validate=validate.Range(min=1))  # in minutes
    departure_time = fields.DateTime(required=False)
    departure_airport_id = fields.Int(required=False, validate=validate.Range(min=1))
    arrival_airport_id = fields.Int(required=False, validate=validate.Range(min=1))
    price = fields.Decimal(required=False, validate=validate.Range(min=0.01))
    total_seats = fields.Int(required=False, validate=validate.Range(min=1))
    rejection_reason = fields.Str(required=False)
    approved_by = fields.Int(required=False, validate=validate.Range(min=1))
    actual_start_time = fields.DateTime(required=False)

    @validates('departure_time')
    def validate_departure_time(self, value):
        if value and value < datetime.now(timezone.utc):
            raise ValidationError('Departure time must be in the future')


def validate_update_flight_data(data: Dict[str, Any]) -> FlightUpdateDTO:
    """Validate and load flight update data into a data object."""
    schema = FlightUpdateValidationSchema()
    errors = schema.validate(data)
    if errors:
        raise ValueError(errors)
    
    validated_dict: Dict[str, Any] = cast(Dict[str, Any], schema.load(data))
    return FlightUpdateDTO(**validated_dict)


class FlightStatusUpdateValidationSchema(Schema):
    """Validation schema for flight status update data"""
    status = fields.Str(required=True, validate=validate.OneOf([e.value for e in FlightStatus]))
    rejection_reason = fields.Str(required=False)


def validate_update_flight_status_data(data: Dict[str, Any], admin_id: int) -> FlightStatusUpdateDTO:
    """
    Validate and load flight status update data into a data object.
    
    Args:
        data: The data to validate
        admin_id: The admin ID from headers
        
    Returns:
        FlightStatusUpdateDTO: The validated data transfer object
        
    Raises:
        ValueError: If the data is invalid
    """
    schema = FlightStatusUpdateValidationSchema()
    errors = schema.validate(data)
    if errors:
        raise ValueError(errors)
    
    validated_dict: Dict[str, Any] = cast(Dict[str, Any], schema.load(data))
    return FlightStatusUpdateDTO(**validated_dict)


def validate_cancel_flight_data(admin_id: int, cancellation_reason: Optional[str] = None) -> Dict[str, Any]:
    """
    Validate flight cancellation request.
    
    Args:
        admin_id: The admin ID from headers
        cancellation_reason: Optional reason for cancellation
        
    Returns:
        Dict: Validated cancellation data
        
    Raises:
        ValueError: If admin_id is invalid
    """
    if admin_id < 1:
        raise ValueError({'error': 'Invalid admin ID'})
    
    return {
        'admin_id': admin_id,
        'cancellation_reason': cancellation_reason
    }
from marshmallow import Schema, fields, validate
from ...domain.dtos.airport_dto import AirportCreateDTO
from typing import Dict, Any, cast


class AirportCreateValidationSchema(Schema):
    """Validation schema for airport creation data"""
    name = fields.Str(required=True, validate=validate.Length(min=3, max=255))
    code = fields.Str(required=True, validate=validate.Length(min=3, max=10))


def validate_create_airport_data(data: Dict[str, Any]) -> AirportCreateDTO:
    """Validate and load airport creation data into a data object."""
    schema = AirportCreateValidationSchema()
    errors = schema.validate(data)
    if errors:
        raise ValueError(errors)
    
    validated_dict: Dict[str, Any] = cast(Dict[str, Any], schema.load(data))
    return AirportCreateDTO(
        name=validated_dict['name'],
        code=validated_dict['code']
    )
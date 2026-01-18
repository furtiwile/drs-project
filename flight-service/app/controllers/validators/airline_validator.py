from marshmallow import Schema, fields, validate
from ...domain.dtos.airline_dto import AirlineCreateDTO, AirlineUpdateDTO
from typing import Dict, Any, cast


class AirlineCreateValidationSchema(Schema):
    """Validation schema for airline creation data"""
    name = fields.Str(required=True, validate=validate.Length(min=2, max=255))


class AirlineUpdateValidationSchema(Schema):
    """Validation schema for airline update data"""
    name = fields.Str(required=False, validate=validate.Length(min=2, max=255))


def validate_create_airline_data(data: Dict[str, Any]) -> AirlineCreateDTO:
    """Validate and load airline creation data into a data object."""
    schema = AirlineCreateValidationSchema()
    errors = schema.validate(data)
    if errors:
        raise ValueError(errors)
    
    validated_dict: Dict[str, Any] = cast(Dict[str, Any], schema.load(data))
    return AirlineCreateDTO(
        name=validated_dict['name']
    )


def validate_update_airline_data(data: Dict[str, Any]) -> AirlineUpdateDTO:
    """Validate and load airline update data into a data object."""
    schema = AirlineUpdateValidationSchema()
    errors = schema.validate(data)
    if errors:
        raise ValueError(errors)
    
    validated_dict: Dict[str, Any] = cast(Dict[str, Any], schema.load(data))
    return AirlineUpdateDTO(
        name=validated_dict.get('name')
    )
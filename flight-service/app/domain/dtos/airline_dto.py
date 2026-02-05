from marshmallow import Schema, fields, validate
from dataclasses import dataclass
from typing import Optional


@dataclass
class AirlineCreateDTO:
    """Data transfer object for validated airline creation data."""
    name: str


@dataclass
class AirlineUpdateDTO:
    """Data transfer object for airline update data with optional fields."""
    name: Optional[str] = None


class AirlineUpdateValidationSchema(Schema):
    """Validation schema for airline update data"""
    name = fields.Str(required=False, validate=validate.Length(min=2, max=255))


class AirlineResponseDTO(Schema):
    """DTO for airline response"""
    id = fields.Int()
    name = fields.Str()
    created_at = fields.DateTime()

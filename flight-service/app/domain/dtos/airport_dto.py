from marshmallow import Schema, fields, validate
from dataclasses import dataclass
from typing import Optional

@dataclass
class AirportCreateDTO:
    """Data transfer object for validated airport creation data."""
    name: str
    code: str

@dataclass
class AirportUpdateDTO:
    """Data transfer object for airport update data with optional fields."""
    name: Optional[str] = None
    code: Optional[str] = None

class AirportUpdateSchema(Schema):
    """Schema for updating airport information"""
    name = fields.Str(required=False, validate=validate.Length(min=3, max=255))
    code = fields.Str(required=False, validate=validate.Length(min=3, max=10))


class AirportResponseDTO(Schema):
    """DTO for airport response"""
    id = fields.Int()
    name = fields.Str()
    code = fields.Str()
    created_at = fields.DateTime()

from typing import List
from marshmallow import Schema, fields, validate, ValidationError, validates_schema
from dataclasses import dataclass


@dataclass
class ReportRequestDTO:
    """Data transfer object for validated report request data."""
    report_types: List[str]


class ReportRequestValidationSchema(Schema):
    """Validation schema for report request data"""
    report_types = fields.List(
        fields.Str(),
        required=True,
        validate=validate.Length(min=1, error="At least one report type must be selected")
    )

    @validates_schema
    def validate_report_types(self, data, **kwargs):
        """Validate that all report types are valid"""
        valid_types = {"upcoming", "in_progress", "completed"}
        report_types = data.get('report_types', [])
        
        if not report_types:
            raise ValidationError("At least one report type must be selected", field_name="report_types")
        
        invalid_types = set(report_types) - valid_types
        if invalid_types:
            raise ValidationError(
                f"Invalid report type(s): {', '.join(invalid_types)}. Valid types are: {', '.join(valid_types)}",
                field_name="report_types"
            )
        
        # Check for duplicates
        if len(report_types) != len(set(report_types)):
            raise ValidationError("Duplicate report types are not allowed", field_name="report_types")

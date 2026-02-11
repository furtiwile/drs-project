from marshmallow import ValidationError
from app.domain.dtos.report_dto import ReportRequestDTO, ReportRequestValidationSchema
from typing import Dict, List, cast

def validate_report_data(data: Dict[str, List[str]]) -> ReportRequestDTO:
    schema = ReportRequestValidationSchema()
    try:
        validated_dict: Dict[str, List[str]] = cast(Dict[str, List[str]], schema.load(data))
        return ReportRequestDTO(
            report_types=validated_dict['report_types']
        )
    except ValidationError as e:
        raise ValueError({'error': 'Validation error', 'details': e.messages})
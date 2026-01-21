from typing import Dict, Optional
from ..models.enums import FlightStatus


class FlightValidator:
    """Validator class for flight-related business rules and data validation."""

    @staticmethod
    def validate_filters(filters: Optional[Dict]) -> Optional[Dict]:
        """Validate and clean filter parameters for flight queries."""
        if not filters:
            return filters
        
        cleaned = filters.copy()
        
        if 'status' in cleaned:
            if cleaned['status'] not in FlightStatus:
                del cleaned['status']
        
        if 'min_price' in cleaned and cleaned['min_price'] < 0:
            del cleaned['min_price']
        if 'max_price' in cleaned and cleaned['max_price'] < 0:
            del cleaned['max_price']
        
        if ('min_price' in cleaned and 'max_price' in cleaned and 
            cleaned['min_price'] > cleaned['max_price']):
            cleaned['min_price'], cleaned['max_price'] = cleaned['max_price'], cleaned['min_price']
        
        return cleaned

    @staticmethod
    def validate_status_transition(current_status: FlightStatus, new_status: FlightStatus, rejection_reason: Optional[str]) -> bool:
        """Validate flight status transition."""
        
        if new_status not in FlightStatus:
            return False
        
        if new_status == FlightStatus.REJECTED and not rejection_reason:
            return False
        
        if current_status in [FlightStatus.COMPLETED, FlightStatus.CANCELLED] and \
           new_status in [FlightStatus.APPROVED, FlightStatus.REJECTED  ]:
            return False
        
        return True
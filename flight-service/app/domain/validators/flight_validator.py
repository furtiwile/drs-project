from typing import Dict, Optional
from ..enums.flight_status import FlightStatus


class FlightValidator:
    """Validator class for flight-related business rules and data validation."""

    @staticmethod
    def validate_filters(filters: Optional[Dict]) -> Optional[Dict]:
        """Validate and clean filter parameters for flight queries."""
        if not filters:
            return filters
        
        cleaned = filters.copy()
        
        # Validate status filter
        if 'status' in cleaned:
            valid_statuses = [status.value for status in FlightStatus]
            if cleaned['status'] not in valid_statuses:
                del cleaned['status']
        
        # Validate price filters
        if 'min_price' in cleaned and cleaned['min_price'] < 0:
            del cleaned['min_price']
        if 'max_price' in cleaned and cleaned['max_price'] < 0:
            del cleaned['max_price']
        
        # Ensure min_price <= max_price
        if ('min_price' in cleaned and 'max_price' in cleaned and 
            cleaned['min_price'] > cleaned['max_price']):
            cleaned['min_price'], cleaned['max_price'] = cleaned['max_price'], cleaned['min_price']
        
        return cleaned

    @staticmethod
    def validate_status_transition(current_status: str, new_status: str, rejection_reason: Optional[str]) -> bool:
        """Validate flight status transition with business rules."""
        valid_statuses = [status.value for status in FlightStatus]
        
        # Validate new status is valid
        if new_status not in valid_statuses:
            return False
        
        # Validate rejection reason is provided when status is REJECTED
        if new_status == FlightStatus.REJECTED.value and not rejection_reason:
            return False
        
        # Business logic: Can't approve/reject a completed or cancelled flight
        if current_status in [FlightStatus.COMPLETED.value, FlightStatus.CANCELLED.value] and \
           new_status in [FlightStatus.APPROVED.value, FlightStatus.REJECTED.value]:
            return False
        
        return True
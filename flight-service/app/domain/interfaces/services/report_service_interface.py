from abc import ABC, abstractmethod
from typing import List


class ReportServiceInterface(ABC):
    """Interface for report generation service"""

    @abstractmethod
    def generate_flight_report(self, report_types: List[str]) -> bytes:
        """
        Generate PDF report for specified flight report types.
        
        Args:
            report_types: List of report types to include ('upcoming', 'in_progress', 'completed')
            
        Returns:
            PDF file as bytes
        """
        pass

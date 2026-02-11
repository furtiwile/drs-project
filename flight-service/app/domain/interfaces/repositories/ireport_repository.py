from abc import ABC, abstractmethod
from typing import List
from app.domain.models.flights import Flight


class IReportRepository(ABC):
    """Interface for report data repository"""

    @abstractmethod
    def get_upcoming_flights(self) -> List[Flight]:
        """
        Get all upcoming flights (APPROVED status, not yet departed).
        
        Returns:
            List of Flight objects with eager-loaded relationships (airline, airports)
        """
        pass

    @abstractmethod
    def get_in_progress_flights(self) -> List[Flight]:
        """
        Get all in-progress flights (IN_PROGRESS status).
        
        Returns:
            List of Flight objects with eager-loaded relationships (airline, airports)
        """
        pass

    @abstractmethod
    def get_completed_flights(self) -> List[Flight]:
        """
        Get all completed and cancelled flights (COMPLETED or CANCELLED status).
        
        Returns:
            List of Flight objects with eager-loaded relationships (airline, airports)
        """
        pass

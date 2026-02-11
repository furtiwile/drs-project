from abc import ABC, abstractmethod
from typing import Any

class ReportControllerInterface(ABC):
    @abstractmethod
    def generate_flight_report(self) -> Any:
        pass
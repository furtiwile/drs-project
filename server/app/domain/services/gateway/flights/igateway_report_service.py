from abc import ABC, abstractmethod

from app.domain.dtos.gateway.flights.report.report_request_dto import ReportRequestDTO
from app.domain.types.result import Result

class IGatewayReportService(ABC):
    @abstractmethod
    def generate_pdf_report(self, data: ReportRequestDTO, admin_id: int) -> Result[None, int]:
        pass
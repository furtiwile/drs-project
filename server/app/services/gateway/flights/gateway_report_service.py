from app.database import get_db

from app.domain.services.gateway.flights.igateway_report_service import IGatewayReportService
from app.domain.services.mail.imail_service import IMailService
from app.domain.repositories.user.iuser_repository import IUserRepository
from app.domain.dtos.gateway.flights.report.report_request_dto import ReportRequestDTO
from app.domain.types.result import Result, err, ok

from app.services.mail.mail_formatter import MailFormatter

from app.infrastructure.gateway.gateway_client import GatewayClient
from app.infrastructure.gateway.utils.api_callers import make_api_call

class GatewayReportService(IGatewayReportService):
    def __init__(self, gateway_client: GatewayClient, user_repository: IUserRepository, mail_service: IMailService) -> None:
        self.client = gateway_client
        self.user_repository = user_repository
        self.mail_service = mail_service

    def generate_pdf_report(self, data: ReportRequestDTO, admin_id: int) -> Result[None, int]:
        result = make_api_call(
            lambda: self.client.post("/reports/flights", headers={'admin-id': str(admin_id)}, json=data.to_dict(), timeout=20),
            lambda r: r.content
        )
        if isinstance(result, ok):
            pdf_bytes: bytes = result.data

            with get_db() as db:
                user = self.user_repository.get_by_id(admin_id, db)

            if user is None:
                return err(404, "User not found")

            self.mail_service.send_async(
                user.email, 
                MailFormatter.flight_report_format(user), 
                attachment_bytes=pdf_bytes, 
                attachment_name="flight_report.pdf"
            )

            return ok(None)
        
        return err(result.status_code, result.message)
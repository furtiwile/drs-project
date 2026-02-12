from flask import Blueprint, Response, g, request

from app.domain.dtos.gateway.flights.report.report_request_dto import ReportRequestDTO
from app.domain.services.gateway.flights.igateway_report_service import IGatewayReportService
from app.domain.enums.role import Role

from app.middlewares.json.json_middleware import require_json
from app.middlewares.authentication.authentication import authenticate
from app.middlewares.authorization.authorization import authorize

from app.web_api.controllers.auth.auth_controller import handle_response

class GatewayReportController:
    def __init__(self, gateway_report_service: IGatewayReportService) -> None:
        self._gateway_report_blueprint = Blueprint('reports', __name__, url_prefix='/api/v1')
        self.gateway_report_service = gateway_report_service
        self._register_routes()
    
    def _register_routes(self) -> None:
        self._gateway_report_blueprint.add_url_rule('/reports/flights', view_func=self.generate_report, methods=['POST'])

    @require_json
    @authenticate
    @authorize(Role.ADMINISTRATOR)
    def generate_report(self) -> tuple[Response, int]:
        data = request.get_json()
        create_report_dto = ReportRequestDTO.from_dict(data)
        admin_id = g.user.user_id

        result = self.gateway_report_service.generate_pdf_report(create_report_dto, admin_id)
        return handle_response(result, success_code=204)

    @property
    def blueprint(self) -> Blueprint:
        return self._gateway_report_blueprint
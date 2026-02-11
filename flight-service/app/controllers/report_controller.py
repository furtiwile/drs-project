"""
Report Controller - PDF Report Generation
Following Clean Architecture and SOLID principles
"""
from flask import Blueprint, request, jsonify, Response
from app.domain.dtos.report_dto import ReportRequestDTO
from app.domain.interfaces.services.report_service_interface import ReportServiceInterface
from app.domain.interfaces.controllers.report_controller_interface import ReportControllerInterface
from app.controllers.validators.header_validator import validate_admin_id_header
from app.controllers.validators.report_validator import validate_report_data
from app.utils.logger_service import get_logger, LoggerService
from datetime import datetime
import time

logger = get_logger(__name__)

report_bp = Blueprint('report', __name__)


class ReportController(ReportControllerInterface):
    """Controller for handling PDF report generation requests"""

    def __init__(self, report_service: ReportServiceInterface, blueprint: Blueprint):
        self.report_service = report_service
        self.register_routes(blueprint)

    def generate_flight_report(self):
        """
        POST /reports/flights
        Generate PDF report for flights (ADMINISTRATOR only)
        
        Request body:
        {
            "report_types": ["upcoming", "in_progress", "completed"]
        }
        
        Response: PDF file (application/pdf)
        """
        start_time = time.time()
        LoggerService.log_request(logger, 'POST', '/reports/flights')
        
        # Validate admin authorization
        try:
            admin_id = validate_admin_id_header(request.headers.get('admin-id'))
            LoggerService.log_with_context(logger, 'DEBUG', 'Admin authorization validated',
                                         admin_id=admin_id)
        except ValueError as e:
            duration_ms = (time.time() - start_time) * 1000
            LoggerService.log_response(logger, 'POST', '/reports/flights', 401, duration_ms,
                                     error='Unauthorized - Admin ID required')
            return jsonify(e.args[0]), 401
        
        # Get and validate request data
        data = request.get_json()
        if not data:
            duration_ms = (time.time() - start_time) * 1000
            LoggerService.log_response(logger, 'POST', '/reports/flights', 400, duration_ms,
                                     error='Invalid JSON')
            return jsonify({'error': 'Invalid JSON'}), 400
        
        # Validate report request
        try:
            validated_data: ReportRequestDTO = validate_report_data(data)
            report_types = validated_data.report_types
            LoggerService.log_with_context(logger, 'DEBUG', 'Report request validated',
                                         report_types=report_types,
                                         admin_id=admin_id)
        except ValueError as e:
            duration_ms = (time.time() - start_time) * 1000
            LoggerService.log_response(logger, 'POST', '/reports/flights', 400, duration_ms,
                                     error='Validation failed')
            return jsonify(e.args[0]), 400
        
        # Generate PDF report
        try:
            pdf_bytes = self.report_service.generate_flight_report(report_types)
            
            LoggerService.log_business_event(logger, 'REPORT_GENERATED',
                                           admin_id=admin_id,
                                           report_types=report_types,
                                           size_bytes=len(pdf_bytes))
            
            # Create filename with timestamp
            timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
            filename = f"flight_report_{timestamp}.pdf"
            
            duration_ms = (time.time() - start_time) * 1000
            LoggerService.log_response(logger, 'POST', '/reports/flights', 200, duration_ms,
                                     filename=filename)
            
            # Return PDF as response
            return Response(
                pdf_bytes,
                mimetype='application/pdf',
                headers={
                    'Content-Disposition': f'attachment; filename="{filename}"',
                    'Content-Type': 'application/pdf'
                }
            )
        except Exception as e:
            duration_ms = (time.time() - start_time) * 1000
            LoggerService.log_with_context(logger, 'ERROR', 'Failed to generate report',
                                         error=str(e),
                                         admin_id=admin_id)
            LoggerService.log_response(logger, 'POST', '/reports/flights', 500, duration_ms,
                                     error='Report generation failed')
            return jsonify({'error': 'Failed to generate report', 'details': str(e)}), 500

    def register_routes(self, blueprint: Blueprint):
        """Register all report routes"""
        blueprint.add_url_rule(
            '/reports/flights',
            'generate_flight_report',
            self.generate_flight_report,
            methods=['POST']
        )


def create_report_controller(report_service: ReportServiceInterface) -> ReportController:
    """Factory function to create report controller"""
    return ReportController(report_service, report_bp)

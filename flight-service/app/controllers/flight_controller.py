"""
Flight Controller - Updated with new features
Following Clean Architecture and SOLID principles
"""
from flask import Blueprint, request, jsonify
from ..domain.dtos.flight_dto import (
    FlightCreateDTO, 
    FlightUpdateDTO, 
    FlightStatusUpdateDTO,
    FlightResponseDTO
)
from app.domain.interfaces.services.flight_service_interface import FlightServiceInterface
from app.domain.interfaces.controllers.flight_controller_interface import FlightControllerInterface
from .validators.flight_validator import validate_create_flight_data, validate_update_flight_data, validate_update_flight_status_data
from .validators.header_validator import validate_admin_id_header, validate_user_id_header  # Assuming validate_user_id_header is added to header_validator.py
from app.utils.logger_service import get_logger, LoggerService
import time

logger = get_logger(__name__)

flight_bp = Blueprint('flight', __name__)


class FlightController(FlightControllerInterface):
    def __init__(self, flight_service: FlightServiceInterface, blueprint: Blueprint):
        self.flight_service = flight_service
        self.register_routes(blueprint)

    def create_flight(self):
        """
        POST /flights
        Creates a new flight (MANAGER only)
        
        The flight is created with PENDING status and admins are notified via WebSocket
        """
        start_time = time.time()
        LoggerService.log_request(logger, 'POST', '/flights')
        
        data = request.get_json()
        if not data:
            duration_ms = (time.time() - start_time) * 1000
            LoggerService.log_response(logger, 'POST', '/flights', 400, duration_ms, error='Invalid JSON')
            return jsonify({'error': 'Invalid JSON'}), 400
        
        try:
            user_id = validate_user_id_header(request.headers.get('user-id'))
        except ValueError as e:
            duration_ms = (time.time() - start_time) * 1000
            LoggerService.log_response(logger, 'POST', '/flights', 400, duration_ms, error='Invalid user-id header')
            return jsonify(e.args[0]), 400
        
        try:
            validated_data: FlightCreateDTO = validate_create_flight_data(data)
            LoggerService.log_with_context(logger, 'DEBUG', 'Flight data validated', 
                                         flight_name=data.get('flight_name'),
                                         user_id=user_id)
        except ValueError as e:
            duration_ms = (time.time() - start_time) * 1000
            LoggerService.log_response(logger, 'POST', '/flights', 400, duration_ms, error='Validation failed')
            return jsonify(e.args[0]), 400
        
        flight = self.flight_service.create_flight(validated_data, user_id)
        if not flight:
            duration_ms = (time.time() - start_time) * 1000
            LoggerService.log_response(logger, 'POST', '/flights', 400, duration_ms, error='Flight creation failed')
            return jsonify({'error': 'Failed to create flight'}), 400
        
        LoggerService.log_business_event(logger, 'FLIGHT_CREATED', 
                                       flight_id=flight.flight_id,
                                       flight_name=flight.flight_name,
                                       user_id=user_id)
        
        response_dto = FlightResponseDTO()
        duration_ms = (time.time() - start_time) * 1000
        LoggerService.log_response(logger, 'POST', '/flights', 201, duration_ms, flight_id=flight.flight_id)
        return jsonify(response_dto.dump(flight)), 201

    def get_flight(self, flight_id: int):
        """GET /flights/<int:flight_id> - Retrieve a flight by ID"""
        start_time = time.time()
        LoggerService.log_request(logger, 'GET', f'/flights/{flight_id}', flight_id=flight_id)
        
        flight = self.flight_service.get_flight(flight_id)
        if not flight:
            duration_ms = (time.time() - start_time) * 1000
            LoggerService.log_response(logger, 'GET', f'/flights/{flight_id}', 404, duration_ms)
            return jsonify({'error': 'Flight not found'}), 404
        
        response_dto = FlightResponseDTO()
        duration_ms = (time.time() - start_time) * 1000
        LoggerService.log_response(logger, 'GET', f'/flights/{flight_id}', 200, duration_ms)
        return jsonify(response_dto.dump(flight))

    def get_all_flights(self):
        """
        GET /flights
        Retrieves all flights with pagination and optional filters
        """
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        
        if page < 1:
            return jsonify({'error': 'Page must be greater than 0'}), 400
        if per_page < 1 or per_page > 100:
            return jsonify({'error': 'Per page must be between 1 and 100'}), 400
        
        filters = {}
        if request.args.get('flight_name'):
            filters['flight_name'] = request.args.get('flight_name')
        if request.args.get('airline_id'):
            filters['airline_id'] = request.args.get('airline_id', type=int)
        if request.args.get('status'):
            filters['status'] = request.args.get('status')
        if request.args.get('departure_airport_id'):
            filters['departure_airport_id'] = request.args.get('departure_airport_id', type=int)
        if request.args.get('arrival_airport_id'):
            filters['arrival_airport_id'] = request.args.get('arrival_airport_id', type=int)
        if request.args.get('min_price'):
            filters['min_price'] = request.args.get('min_price', type=float)
        if request.args.get('max_price'):
            filters['max_price'] = request.args.get('max_price', type=float)
        if request.args.get('departure_date'):
            filters['departure_date'] = request.args.get('departure_date')
        
        result = self.flight_service.get_all_flights(page, per_page, filters if filters else None)
        response_dto = FlightResponseDTO(many=True)
        
        return jsonify({
            'flights': response_dto.dump(result['flights']),
            'page': result['page'],
            'per_page': result['per_page'],
            'total': result['total'],
            'pages': result['pages']
        })
    
    def get_flights_by_tab(self):
        """
        GET /flights/tabs/<tab>
        Get flights organized by tab:
        - upcoming: Approved flights that haven't started
        - in-progress: Flights currently in progress with timer
        - completed: Completed and cancelled flights
        """
        tab = request.view_args.get('tab', 'upcoming') if request.view_args else 'upcoming'
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        
        valid_tabs = ['upcoming', 'in-progress', 'completed']
        if tab not in valid_tabs:
            return jsonify({'error': f'Invalid tab. Must be one of: {", ".join(valid_tabs)}'}), 400
        
        if page < 1:
            return jsonify({'error': 'Page must be greater than 0'}), 400
        if per_page < 1 or per_page > 100:
            return jsonify({'error': 'Per page must be between 1 and 100'}), 400
        
        filters = {}
        if request.args.get('flight_name'):
            filters['flight_name'] = request.args.get('flight_name')
        if request.args.get('airline_id'):
            filters['airline_id'] = request.args.get('airline_id', type=int)
        
        result = self.flight_service.get_flights_by_tab(tab, page, per_page, filters if filters else None)
        response_dto = FlightResponseDTO(many=True)
        
        return jsonify({
            'tab': tab,
            'flights': response_dto.dump(result['flights']),
            'page': result['page'],
            'per_page': result['per_page'],
            'total': result['total'],
            'pages': result['pages']
        })
    
    def get_flight_remaining_time(self, flight_id: int):
        """
        GET /flights/<int:flight_id>/remaining-time
        Get remaining time for in-progress flight
        """
        result = self.flight_service.get_flight_remaining_time(flight_id)
        if not result:
            return jsonify({'error': 'Flight not found or not in progress'}), 404
        
        return jsonify(result)

    def update_flight(self, flight_id: int):
        """
        PUT /flights/<int:flight_id>
        Updates a flight (MANAGER only, for PENDING or REJECTED flights)
        """
        start_time = time.time()
        LoggerService.log_request(logger, 'PUT', f'/flights/{flight_id}', flight_id=flight_id)
        
        data = request.get_json()
        if not data:
            duration_ms = (time.time() - start_time) * 1000
            LoggerService.log_response(logger, 'PUT', f'/flights/{flight_id}', 400, duration_ms, error='Invalid JSON')
            return jsonify({'error': 'Invalid JSON'}), 400
        
        try:
            user_id = validate_user_id_header(request.headers.get('user-id'))
        except ValueError as e:
            duration_ms = (time.time() - start_time) * 1000
            LoggerService.log_response(logger, 'PUT', f'/flights/{flight_id}', 400, duration_ms, error='Invalid user-id header')
            return jsonify(e.args[0]), 400
        
        try:
            validated_data: FlightUpdateDTO = validate_update_flight_data(data)
            validated_data.approved_by = user_id  
        except ValueError as e:
            duration_ms = (time.time() - start_time) * 1000
            LoggerService.log_response(logger, 'PUT', f'/flights/{flight_id}', 400, duration_ms, error='Validation failed')
            return jsonify(e.args[0]), 400
        
        flight = self.flight_service.update_flight(flight_id, validated_data)
        if not flight:
            duration_ms = (time.time() - start_time) * 1000
            LoggerService.log_response(logger, 'PUT', f'/flights/{flight_id}', 404, duration_ms, error='Flight not found or update failed')
            return jsonify({'error': 'Flight not found or update failed'}), 404
        
        response_dto = FlightResponseDTO()
        duration_ms = (time.time() - start_time) * 1000
        LoggerService.log_response(logger, 'PUT', f'/flights/{flight_id}', 200, duration_ms)
        return jsonify(response_dto.dump(flight)), 200

    def update_flight_status(self, flight_id: int):
        """
        PUT /flights/<int:flight_id>/status
        Updates the status of a flight (ADMIN only - approve/reject)
        
        Admins can approve or reject pending flights.
        Manager is notified via WebSocket when status changes.
        
        Headers:
            admin-id: integer (required)
        """
        start_time = time.time()
        data = request.get_json()
        if not data:
            duration_ms = (time.time() - start_time) * 1000
            LoggerService.log_response(logger, 'PUT', f'/flights/{flight_id}/status', 400, duration_ms, error='Invalid JSON')
            return jsonify({'error': 'Invalid JSON'}), 400
        
        try:
            admin_id = validate_admin_id_header(request.headers.get('admin-id'))
        except ValueError as e:
            duration_ms = (time.time() - start_time) * 1000
            LoggerService.log_response(logger, 'PUT', f'/flights/{flight_id}/status', 400, duration_ms, error='Invalid admin-id header')
            return jsonify(e.args[0]), 400
        
        LoggerService.log_request(logger, 'PUT', f'/flights/{flight_id}/status', 
                                flight_id=flight_id, admin_id=admin_id)
        
        try:
            validated_data: FlightStatusUpdateDTO = validate_update_flight_status_data(data, admin_id)
        except ValueError as e:
            duration_ms = (time.time() - start_time) * 1000
            LoggerService.log_response(logger, 'PUT', f'/flights/{flight_id}/status', 400, duration_ms)
            return jsonify(e.args[0]), 400
        
        flight = self.flight_service.update_flight_status(flight_id, validated_data, admin_id)
        if not flight:
            duration_ms = (time.time() - start_time) * 1000
            LoggerService.log_response(logger, 'PUT', f'/flights/{flight_id}/status', 400, duration_ms)
            return jsonify({'error': 'Flight not found or status update failed'}), 400
        
        LoggerService.log_business_event(logger, 'FLIGHT_STATUS_UPDATED',
                                       flight_id=flight_id,
                                       new_status=flight.status.value,
                                       admin_id=admin_id)
        
        response_dto = FlightResponseDTO()
        duration_ms = (time.time() - start_time) * 1000
        LoggerService.log_response(logger, 'PUT', f'/flights/{flight_id}/status', 200, duration_ms)
        return jsonify(response_dto.dump(flight)), 200
    
    def cancel_flight(self, flight_id: int):
        """
        POST /flights/<int:flight_id>/cancel
        Cancel an approved flight (ADMIN only)
        
        Can only cancel approved flights that haven't started yet.
        Users who booked the flight will be notified via email.
        
        Headers:
            admin-id: integer (required)
        
        Request JSON (optional):
        {
            "cancellation_reason": "string (optional)"
        }
        """
        start_time = time.time()
        data = request.get_json() or {}
        
        # Get and validate admin ID from header
        try:
            admin_id = validate_admin_id_header(request.headers.get('admin-id'))
        except ValueError as e:
            duration_ms = (time.time() - start_time) * 1000
            LoggerService.log_response(logger, 'POST', f'/flights/{flight_id}/cancel', 400, duration_ms, error='Invalid admin-id header')
            return jsonify(e.args[0]), 400
        
        LoggerService.log_request(logger, 'POST', f'/flights/{flight_id}/cancel',
                                flight_id=flight_id, admin_id=admin_id)
        
        flight = self.flight_service.cancel_flight(flight_id, admin_id)
        if not flight:
            duration_ms = (time.time() - start_time) * 1000
            LoggerService.log_response(logger, 'POST', f'/flights/{flight_id}/cancel', 400, duration_ms)
            return jsonify({'error': 'Flight not found or cannot be cancelled'}), 400
        
        LoggerService.log_business_event(logger, 'FLIGHT_CANCELLED',
                                       flight_id=flight_id,
                                       flight_name=flight.flight_name,
                                       admin_id=admin_id)
        
        response_dto = FlightResponseDTO()
        duration_ms = (time.time() - start_time) * 1000
        LoggerService.log_response(logger, 'POST', f'/flights/{flight_id}/cancel', 200, duration_ms)
        return jsonify({
            'message': 'Flight cancelled successfully',
            'flight': response_dto.dump(flight)
        }), 200

    def delete_flight(self, flight_id: int):
        """
        DELETE /flights/<int:flight_id>
        Deletes a flight by ID (ADMIN only)
        """
        start_time = time.time()
        LoggerService.log_request(logger, 'DELETE', f'/flights/{flight_id}', flight_id=flight_id)
        
        # Get and validate user ID from header (assuming ADMIN role check in service)
        try:
            user_id = validate_user_id_header(request.headers.get('user-id'))
        except ValueError as e:
            duration_ms = (time.time() - start_time) * 1000
            LoggerService.log_response(logger, 'DELETE', f'/flights/{flight_id}', 400, duration_ms, error='Invalid user-id header')
            return jsonify(e.args[0]), 400
        
        success = self.flight_service.delete_flight(flight_id)
        if not success:
            duration_ms = (time.time() - start_time) * 1000
            LoggerService.log_response(logger, 'DELETE', f'/flights/{flight_id}', 400, duration_ms, error='Flight not found or deletion failed')
            return jsonify({'error': 'Flight not found or deletion failed'}), 400
        
        duration_ms = (time.time() - start_time) * 1000
        LoggerService.log_response(logger, 'DELETE', f'/flights/{flight_id}', 200, duration_ms)
        return jsonify({'message': 'Flight deleted'}), 200

    def get_available_seats(self, flight_id: int):
        """
        GET /flights/<int:flight_id>/available-seats
        Retrieves the number of available seats for a flight
        """
        available_seats = self.flight_service.get_available_seats(flight_id)
        return jsonify({'flight_id': flight_id, 'available_seats': available_seats})

    def register_routes(self, bp: Blueprint):
        """Register routes to the blueprint."""
        bp.add_url_rule('/flights', 'create_flight', self.create_flight, methods=['POST'])
        bp.add_url_rule('/flights', 'get_all_flights', self.get_all_flights, methods=['GET'])
        bp.add_url_rule('/flights/tabs/<string:tab>', 'get_flights_by_tab', self.get_flights_by_tab, methods=['GET'])
        bp.add_url_rule('/flights/<int:flight_id>', 'get_flight', self.get_flight, methods=['GET'])
        bp.add_url_rule('/flights/<int:flight_id>', 'update_flight', self.update_flight, methods=['PATCH', 'PUT'])
        bp.add_url_rule('/flights/<int:flight_id>/status', 'update_flight_status', self.update_flight_status, methods=['PATCH', 'PUT'])
        bp.add_url_rule('/flights/<int:flight_id>/cancel', 'cancel_flight', self.cancel_flight, methods=['POST'])
        bp.add_url_rule('/flights/<int:flight_id>', 'delete_flight', self.delete_flight, methods=['DELETE'])
        bp.add_url_rule('/flights/<int:flight_id>/available-seats', 'get_available_seats', self.get_available_seats, methods=['GET'])
        bp.add_url_rule('/flights/<int:flight_id>/remaining-time', 'get_flight_remaining_time', self.get_flight_remaining_time, methods=['GET'])

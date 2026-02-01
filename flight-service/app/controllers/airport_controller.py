import string
from flask import Blueprint, request, jsonify
from typing import Optional
from ..domain.dtos.airport_dto import AirportUpdateDTO, AirportResponseDTO, AirportCreateDTO
from app.domain.interfaces.services.airport_service_interface import AirportServiceInterface
from app.domain.interfaces.controllers.airport_controller_interface import AirportControllerInterface
from .validators.airport_validator import validate_create_airport_data, validate_update_airport_data
from dataclasses import asdict
from app.utils.logger_service import get_logger, LoggerService
import time

logger = get_logger(__name__)
airport_bp = Blueprint('airport', __name__)

class AirportController(AirportControllerInterface):
    def __init__(self, airport_service: AirportServiceInterface, blueprint: Blueprint):
        self.airport_service = airport_service
        self.register_routes(blueprint)

    def create_airport(self):
        """
        POST /airports
        Creates a new airport.

        Request JSON format:
        {
            "name": "string (required, min length 1, max length 100)",
            "code": "string (required, exactly 3 uppercase letters)"
        }

        Returns:
            tuple: JSON response with airport data or error message, and HTTP status code.
        """
        start_time = time.time()
        data = request.get_json()
        if not data:
            duration_ms = (time.time() - start_time) * 1000
            LoggerService.log_response(logger, 'POST', '/airports', 400, duration_ms, error='Invalid JSON')
            return jsonify({'error': 'Invalid JSON'}), 400
        
        LoggerService.log_request(logger, 'POST', '/airports', name=data.get('name'), code=data.get('code'))
        
        try:
            validated_data: AirportCreateDTO = validate_create_airport_data(data)
        except ValueError as e:
            duration_ms = (time.time() - start_time) * 1000
            LoggerService.log_response(logger, 'POST', '/airports', 400, duration_ms, error='Validation failed')
            return jsonify(e.args[0]), 400
        
        airport = self.airport_service.create_airport(validated_data)
        if not airport:
            duration_ms = (time.time() - start_time) * 1000
            LoggerService.log_response(logger, 'POST', '/airports', 400, duration_ms, error='Duplicate airport code')
            return jsonify({'error': 'Airport with this code already exists'}), 400
        
        LoggerService.log_business_event(logger, 'AIRPORT_CREATED',
                                       airport_id=airport.id,
                                       code=airport.code)

        response_dto = AirportResponseDTO()
        duration_ms = (time.time() - start_time) * 1000
        LoggerService.log_response(logger, 'POST', '/airports', 201, duration_ms, airport_id=airport.id)
        return jsonify(response_dto.dump(airport)), 201

    def get_airport(self, airport_id: int):
        """
        GET /airports/<int:airport_id>
        Retrieves an airport by ID.

        Args:
            airport_id (int): The airport ID from the URL.

        Returns:
            tuple: JSON response with airport data or error message, and HTTP status code.
        """
        airport = self.airport_service.get_airport(airport_id)
        if not airport:
            return jsonify({'error': 'Airport not found'}), 404
        response_dto = AirportResponseDTO()
        return jsonify(response_dto.dump(airport))

    def get_all_airports(self):
        """
        GET /airports
        Retrieves all airports with pagination.

        Query parameters:
            page (int): Page number (default: 1)
            per_page (int): Items per page (default: 10)

        Returns:
            Response: JSON response with list of airports and pagination info.
        """
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        
        if page < 1:
            return jsonify({'error': 'Page must be greater than 0'}), 400
        if per_page < 1 or per_page > 100:
            return jsonify({'error': 'Per page must be between 1 and 100'}), 400
        
        result = self.airport_service.get_all_airports(page=page, per_page=per_page)
        response_dto = AirportResponseDTO(many=True)
        return jsonify({
            'airports': response_dto.dump(result['airports']),
            'pagination': {
                'page': result['page'],
                'per_page': result['per_page'],
                'total': result['total'],
                'pages': result['pages']
            }
        })

    def update_airport(self, airport_id: int):
        """
        PATCH /airports/<int:airport_id>
        Updates an airport by ID.

        Args:
            airport_id (int): The airport ID from the URL.

        Request JSON format:
        {
            "name": "string (optional, min length 1, max length 100)",
            "code": "string (optional, exactly 3 uppercase letters)"
        }
        Note: At least one field (name or code) must be provided.

        Returns:
            tuple: JSON response with updated airport data or error message, and HTTP status code.
        """
        data = request.get_json()
        if not data:
            return jsonify({'error': 'Invalid JSON'}), 400
        try:
            validated_data: AirportUpdateDTO = validate_update_airport_data(data)
        except ValueError as e:
            return jsonify(e.args[0]), 400
        
        if validated_data.name is None and validated_data.code is None:
            return jsonify({'error': 'At least one field (name or code) must be provided'}), 400
        
        airport = self.airport_service.update_airport(airport_id, validated_data)
        if not airport:
            return jsonify({'error': 'Airport not found'}), 404
        response_dto = AirportResponseDTO()
        return jsonify(response_dto.dump(airport))

    def delete_airport(self, airport_id: int):
        """
        DELETE /airports/<int:airport_id>
        Deletes an airport by ID.

        Args:
            airport_id (int): The airport ID from the URL.

        Returns:
            tuple: JSON response with success message or error message, and HTTP status code.
        """
        success = self.airport_service.delete_airport(airport_id)
        if not success:
            return jsonify({'error': 'Airport not found'}), 404
        return jsonify({'message': 'Airport deleted'}), 200

    def get_airport_info(self, airport_code: str):
        """
        GET /airports/info/<airport_code>
        Retrieves airport information by code.

        Args:
            airport_code (str): The airport code from the URL.

        Returns:
            tuple: JSON response with airport data or error message, and HTTP status code.
        """
        if not airport_code or len(airport_code) != 3 or not airport_code.isupper() or not airport_code.isalpha():
            return jsonify({'error': 'Airport code must be exactly 3 uppercase letters'}), 400
        
        airport = self.airport_service.fetch_airport_info(airport_code)
        if not airport:
            return jsonify({'error': 'Airport not found'}), 404
        response_dto = AirportResponseDTO()
        return jsonify(response_dto.dump(airport))

    def register_routes(self, bp: Blueprint):
        bp.add_url_rule('/airports', 'create_airport', self.create_airport, methods=['POST'])
        bp.add_url_rule('/airports', 'get_all_airports', self.get_all_airports, methods=['GET'])
        bp.add_url_rule('/airports/<int:airport_id>', 'get_airport', self.get_airport, methods=['GET'])
        bp.add_url_rule('/airports/<int:airport_id>', 'update_airport', self.update_airport, methods=['PATCH'])
        bp.add_url_rule('/airports/<int:airport_id>', 'delete_airport', self.delete_airport, methods=['DELETE'])
        bp.add_url_rule('/airports/info/<airport_code>', 'get_airport_info', self.get_airport_info, methods=['GET'])
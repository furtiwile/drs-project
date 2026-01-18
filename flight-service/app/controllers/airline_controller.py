from flask import Blueprint, request, jsonify
from typing import Optional
from ..domain.dtos.airline_dto import AirlineCreateDTO, AirlineUpdateDTO, AirlineResponseDTO
from app.domain.interfaces.services.airline_service_interface import AirlineServiceInterface
from app.domain.interfaces.controllers.airline_controller_interface import AirlineControllerInterface
from .validators.airline_validator import validate_create_airline_data, validate_update_airline_data
from dataclasses import asdict

airline_bp = Blueprint('airline', __name__)


class AirlineController(AirlineControllerInterface):
    def __init__(self, airline_service: AirlineServiceInterface, blueprint: Blueprint):
        self.airline_service = airline_service
        self.register_routes(blueprint)

    def create_airline(self):
        """
        POST /airlines
        Creates a new airline.

        Data is obtained from the request body JSON.

        Returns:
            tuple: JSON response with airline data or error message, and HTTP status code.
        """
        data = request.get_json()
        try:
            validated_data: AirlineCreateDTO = validate_create_airline_data(data)
        except ValueError as e:
            return jsonify(e.args[0]), 400
        
        airline = self.airline_service.create_airline(validated_data)
        if not airline:
            return jsonify({'error': 'Failed to create airline'}), 400
        
        response_dto = AirlineResponseDTO()
        return jsonify(response_dto.dump(airline)), 201

    def get_airline(self, airline_id: int):
        """
        GET /airlines/<int:airline_id>
        Retrieves an airline by ID.

        Args:
            airline_id (int): The airline ID from the URL.

        Returns:
            tuple: JSON response with airline data or error message, and HTTP status code.
        """
        airline = self.airline_service.get_airline(airline_id)
        if not airline:
            return jsonify({'error': 'Airline not found'}), 404
        
        response_dto = AirlineResponseDTO()
        return jsonify(response_dto.dump(airline))

    def get_all_airlines(self):
        """
        GET /airlines
        Retrieves all airlines with pagination.

        Query parameters:
            page (int): Page number (default: 1)
            per_page (int): Items per page (default: 10)

        Returns:
            Response: JSON response with paginated list of airlines.
        """
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        
        result = self.airline_service.get_all_airlines(page, per_page)
        response_dto = AirlineResponseDTO(many=True)
        
        return jsonify({
            'airlines': response_dto.dump(result['airlines']),
            'page': result['page'],
            'per_page': result['per_page'],
            'total': result['total'],
            'pages': result['pages']
        })

    def update_airline(self, airline_id: int):
        """
        PATCH /airlines/<int:airline_id>
        Updates an airline by ID.

        Args:
            airline_id (int): The airline ID from the URL.

        Data is obtained from the request body JSON.

        Returns:
            tuple: JSON response with updated airline data or error message, and HTTP status code.
        """
        data = request.get_json()
        try:
            validated_data: AirlineUpdateDTO = validate_update_airline_data(data)
        except ValueError as e:
            return jsonify(e.args[0]), 400
        
        # Check if at least one field is provided
        if validated_data.name is None:
            return jsonify({'error': 'At least one field (name) must be provided'}), 400
        
        airline = self.airline_service.update_airline(airline_id, validated_data)
        if not airline:
            return jsonify({'error': 'Airline not found'}), 404
        
        response_dto = AirlineResponseDTO()
        return jsonify(response_dto.dump(airline))

    def delete_airline(self, airline_id: int):
        """
        DELETE /airlines/<int:airline_id>
        Deletes an airline by ID.

        Args:
            airline_id (int): The airline ID from the URL.

        Returns:
            tuple: JSON response with success message or error message, and HTTP status code.
        """
        success = self.airline_service.delete_airline(airline_id)
        if not success:
            return jsonify({'error': 'Airline not found'}), 404
        
        return jsonify({'message': 'Airline deleted'}), 200

    def register_routes(self, bp: Blueprint):
        """Register routes to the blueprint."""
        bp.add_url_rule('/airlines', 'create_airline', self.create_airline, methods=['POST'])
        bp.add_url_rule('/airlines', 'get_all_airlines', self.get_all_airlines, methods=['GET'])
        bp.add_url_rule('/airlines/<int:airline_id>', 'get_airline', self.get_airline, methods=['GET'])
        bp.add_url_rule('/airlines/<int:airline_id>', 'update_airline', self.update_airline, methods=['PATCH'])
        bp.add_url_rule('/airlines/<int:airline_id>', 'delete_airline', self.delete_airline, methods=['DELETE'])

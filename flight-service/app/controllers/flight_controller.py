from flask import Blueprint, request, jsonify
from typing import Optional
from ..domain.dtos.flight_dto import (
    FlightCreateDTO, 
    FlightUpdateDTO, 
    FlightStatusUpdateDTO,
    FlightResponseDTO,
    FlightFilterDTO
)
from app.domain.interfaces.services.flight_service_interface import FlightServiceInterface
from app.domain.interfaces.controllers.flight_controller_interface import FlightControllerInterface
from .validators.flight_validator import validate_create_flight_data, validate_update_flight_data, validate_update_flight_status_data

flight_bp = Blueprint('flight', __name__)


class FlightController(FlightControllerInterface):
    def __init__(self, flight_service: FlightServiceInterface, blueprint: Blueprint):
        self.flight_service = flight_service
        self.register_routes(blueprint)

    def create_flight(self):
        """
        POST /flights
        Creates a new flight.

        Request JSON format:
        {
            "flight_name": "string (required)",
            "airline_id": "integer (required)",
            "departure_airport_id": "integer (required)",
            "arrival_airport_id": "integer (required)",
            "departure_time": "string (required, ISO datetime)",
            "arrival_time": "string (required, ISO datetime)",
            "price": "float (required)",
            "total_seats": "integer (required)"
        }

        Returns:
            tuple: JSON response with flight data or error message, and HTTP status code.
        """
        data = request.get_json()
        try:
            validated_data: FlightCreateDTO = validate_create_flight_data(data)
        except ValueError as e:
            return jsonify(e.args[0]), 400
        
        flight = self.flight_service.create_flight(validated_data)
        if not flight:
            return jsonify({'error': 'Failed to create flight'}), 400
        
        response_dto = FlightResponseDTO()
        return jsonify(response_dto.dump(flight)), 201

    def get_flight(self, flight_id: int):
        """
        GET /flights/<int:flight_id>
        Retrieves a flight by ID.

        Args:
            flight_id (int): The flight ID from the URL.

        Returns:
            tuple: JSON response with flight data or error message, and HTTP status code.
        """
        flight = self.flight_service.get_flight(flight_id)
        if not flight:
            return jsonify({'error': 'Flight not found'}), 404
        
        response_dto = FlightResponseDTO()
        return jsonify(response_dto.dump(flight))

    def get_all_flights(self):
        """
        GET /flights
        Retrieves all flights with pagination and optional filters.

        Query parameters:
            page (int): Page number (default: 1)
            per_page (int): Items per page (default: 10)
            flight_name (str): Filter by flight name
            airline_id (int): Filter by airline ID
            status (str): Filter by flight status
            departure_airport_id (int): Filter by departure airport ID
            arrival_airport_id (int): Filter by arrival airport ID
            min_price (float): Filter by minimum price
            max_price (float): Filter by maximum price
            departure_date (str): Filter by departure date

        Returns:
            Response: JSON response with paginated and filtered list of flights.
        """
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        
        # Extract filter parameters
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

    def update_flight(self, flight_id: int):
        """
        PUT /flights/<int:flight_id>
        Updates a flight.

        Args:
            flight_id (int): The flight ID from the URL.

        Request JSON format:
        {
            "flight_name": "string (optional)",
            "airline_id": "integer (optional)",
            "departure_airport_id": "integer (optional)",
            "arrival_airport_id": "integer (optional)",
            "departure_time": "string (optional, ISO datetime)",
            "arrival_time": "string (optional, ISO datetime)",
            "price": "float (optional)",
            "total_seats": "integer (optional)"
        }

        Returns:
            tuple: JSON response with flight data or error message, and HTTP status code.
        """
        data = request.get_json()
        try:
            validated_data: FlightUpdateDTO = validate_update_flight_data(data)
        except ValueError as e:
            return jsonify(e.args[0]), 400
        
        flight = self.flight_service.update_flight(flight_id, validated_data)
        if not flight:
            return jsonify({'error': 'Flight not found or update failed'}), 404
        
        response_dto = FlightResponseDTO()
        return jsonify(response_dto.dump(flight)), 200

    def update_flight_status(self, flight_id: int):
        """
        PUT /flights/<int:flight_id>/status
        Updates the status of a flight.

        Args:
            flight_id (int): The flight ID from the URL.

        Request JSON format:
        {
            "status": "string (required, e.g., 'scheduled', 'departed', 'arrived', 'cancelled')",
            "rejection_reason": "string (optional, required if status is 'cancelled')"
        }

        Returns:
            tuple: JSON response with success message or error message, and HTTP status code.
        """
        data = request.get_json()
        try:
            validated_data: FlightStatusUpdateDTO = validate_update_flight_status_data(data)
        except ValueError as e:
            return jsonify(e.args[0]), 400
        
        success = self.flight_service.update_flight_status(flight_id, validated_data)
        if not success:
            return jsonify({'error': 'Flight not found or status update failed due to business rule violation'}), 400
        
        return jsonify({'message': 'Flight status updated'}), 200

    def delete_flight(self, flight_id: int):
        """
        DELETE /flights/<int:flight_id>
        Deletes a flight by ID.

        Args:
            flight_id (int): The flight ID from the URL.

        Returns:
            tuple: JSON response with success message or error message, and HTTP status code.
        """
        success = self.flight_service.delete_flight(flight_id)
        if not success:
            return jsonify({'error': 'Flight not found or deletion failed due to business rule violation'}), 400
        
        return jsonify({'message': 'Flight deleted'}), 200

    def get_available_seats(self, flight_id: int):
        """
        GET /flights/<int:flight_id>/available-seats
        Retrieves the number of available seats for a flight.

        Args:
            flight_id (int): The flight ID from the URL.

        Returns:
            Response: JSON response with flight ID and available seats count.
        """
        available_seats = self.flight_service.get_available_seats(flight_id)
        return jsonify({'flight_id': flight_id, 'available_seats': available_seats})

    def register_routes(self, bp: Blueprint):
        """Register routes to the blueprint."""
        bp.add_url_rule('/flights', 'create_flight', self.create_flight, methods=['POST'])
        bp.add_url_rule('/flights', 'get_all_flights', self.get_all_flights, methods=['GET'])
        bp.add_url_rule('/flights/<int:flight_id>', 'get_flight', self.get_flight, methods=['GET'])
        bp.add_url_rule('/flights/<int:flight_id>', 'update_flight', self.update_flight, methods=['PATCH', 'PUT'])
        bp.add_url_rule('/flights/<int:flight_id>/status', 'update_flight_status', self.update_flight_status, methods=['PATCH', 'PUT'])
        bp.add_url_rule('/flights/<int:flight_id>', 'delete_flight', self.delete_flight, methods=['DELETE'])
        bp.add_url_rule('/flights/<int:flight_id>/available-seats', 'get_available_seats', self.get_available_seats, methods=['GET'])

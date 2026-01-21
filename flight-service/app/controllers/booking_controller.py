from flask import Blueprint, request, jsonify
from ..domain.dtos.booking_dto import (
    BookingCreateDTO,
    BookingResponseDTO
)
from app.domain.interfaces.services.booking_service_interface import BookingServiceInterface
from app.domain.interfaces.controllers.booking_controller_interface import BookingControllerInterface
from .validators.booking_validator import validate_create_booking_data
from dataclasses import asdict

booking_bp = Blueprint('booking', __name__)


class BookingController(BookingControllerInterface):
    def __init__(self, booking_service: BookingServiceInterface, blueprint: Blueprint):
        self.booking_service = booking_service
        self.register_routes(blueprint)

    def create_booking(self):
        """
        POST /bookings
        Creates a new booking.

        Request JSON format:
        {
            "flight_id": "integer (required, min 1)"
        }

        Headers:
            user-id: "integer (required)"

        Returns:
            tuple: JSON response with booking data or error message, and HTTP status code.
        """
        data = request.get_json()
        try:
            validated_data: BookingCreateDTO = validate_create_booking_data(data)
        except ValueError as e:
            return jsonify(e.args[0]), 400
        
        print("Received headers:", dict(request.headers))
        
        user_id_str = request.headers.get('user-id')



        if not user_id_str:
            return jsonify({'error': 'user-id header is required'}), 400
        try:
            user_id = int(user_id_str)
        except ValueError:
            return jsonify({'error': 'Invalid user-id in header'}), 400
        
        booking = self.booking_service.create_booking(user_id, validated_data)
        if not booking:
            return jsonify({'error': 'Failed to create booking. Flight not found or no seats available.'}), 400
        
        response_dto = BookingResponseDTO()
        return jsonify(response_dto.dump(booking)), 201

    def get_booking(self, booking_id: int):
        """
        GET /bookings/<int:booking_id>
        Retrieves a booking by ID.

        Args:
            booking_id (int): The booking ID from the URL.

        Returns:
            tuple: JSON response with booking data or error message, and HTTP status code.
        """
        booking = self.booking_service.get_booking(booking_id)
        if not booking:
            return jsonify({'error': 'Booking not found'}), 404
        
        response_dto = BookingResponseDTO()
        return jsonify(response_dto.dump(booking))

    def get_user_bookings(self, user_id: int):
        """
        GET /users/<int:user_id>/bookings
        Retrieves all bookings for a user with pagination.

        Args:
            user_id (int): The user ID from the URL.

        Query parameters:
            page (int): Page number (default: 1)
            per_page (int): Items per page (default: 10)

        Returns:
            Response: JSON response with paginated list of user bookings.
        """
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        
        result = self.booking_service.get_user_bookings(user_id, page, per_page)
        response_dto = BookingResponseDTO(many=True)
        
        return jsonify({
            'bookings': response_dto.dump(result['bookings']),
            'page': result['page'],
            'per_page': result['per_page'],
            'total': result['total'],                                                                                                   
            'pages': result['pages']
        })

    def get_all_bookings(self):
        """
        GET /bookings
        Retrieves all bookings with pagination.

        Query parameters:
            page (int): Page number (default: 1)
            per_page (int): Items per page (default: 10)

        Returns:
            Response: JSON response with paginated list of all bookings.
        """
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        
        result = self.booking_service.get_all_bookings(page, per_page)
        response_dto = BookingResponseDTO(many=True)
        
        return jsonify({
            'bookings': response_dto.dump(result['bookings']),
            'page': result['page'],
            'per_page': result['per_page'],
            'total': result['total'],
            'pages': result['pages']
        })

    def delete_booking(self, booking_id: int):
        """
        DELETE /bookings/<int:booking_id>
        Deletes a booking by ID.

        Args:
            booking_id (int): The booking ID from the URL.

        Returns:
            tuple: JSON response with success message or error message, and HTTP status code.
        """
        success = self.booking_service.delete_booking(booking_id)
        if not success:
            return jsonify({'error': 'Booking not found'}), 404
        
        return jsonify({'message': 'Booking deleted'}), 200

    def register_routes(self, bp: Blueprint):
        """Register routes to the blueprint."""
        bp.add_url_rule('/bookings', 'create_booking', self.create_booking, methods=['POST'])
        bp.add_url_rule('/bookings', 'get_all_bookings', self.get_all_bookings, methods=['GET'])
        bp.add_url_rule('/bookings/<int:booking_id>', 'get_booking', self.get_booking, methods=['GET'])
        bp.add_url_rule('/users/<int:user_id>/bookings', 'get_user_bookings', self.get_user_bookings, methods=['GET'])
        bp.add_url_rule('/bookings/<int:booking_id>', 'delete_booking', self.delete_booking, methods=['DELETE'])

from flask import Blueprint, request, jsonify
from ..domain.dtos.booking_dto import (
    BookingCreateDTO,
    BookingCreateDTOReturn,
    BookingResponseDTO,
    BookingDTO
)
from app.domain.interfaces.services.booking_service_interface import BookingServiceInterface
from app.domain.interfaces.controllers.booking_controller_interface import BookingControllerInterface
from .validators.booking_validator import validate_create_booking_data
from .validators.header_validator import validate_user_id_header
from app.utils.logger_service import get_logger

logger = get_logger(__name__)
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
            tuple: JSON response with booking data, and HTTP status code.
        """
        data = request.get_json()
        if not data:
            return jsonify({'error': 'Invalid JSON'}), 400
        try:
            validated_data: BookingCreateDTO = validate_create_booking_data(data)
        except ValueError as e:
            return jsonify(e.args[0]), 400
        
        try:
            user_id = validate_user_id_header(request.headers.get('user-id'))
        except ValueError as e:
            return jsonify(e.args[0]), 400
        
        booking_result = self.booking_service.create_booking(user_id, validated_data)
        if not booking_result:
            return jsonify({'error': 'Failed to create booking'}), 400
        
        return jsonify(booking_result.to_dict()), 201
    
    def get_booking_task_status(self, task_id: str):
        """
        GET /bookings/tasks/<task_id>
        Get the status of an async booking task
        
        Returns:
            tuple: JSON response with task status information
        """
        status = self.booking_service.get_booking_task_status(task_id)
        if not status:
            return jsonify({'error': 'Task not found'}), 404
        
        return jsonify(status), 200

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
        
        if page < 1:
            return jsonify({'error': 'Page must be greater than 0'}), 400
        if per_page < 1 or per_page > 100:
            return jsonify({'error': 'Per page must be between 1 and 100'}), 400
        
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
        
        if page < 1:
            return jsonify({'error': 'Page must be greater than 0'}), 400
        if per_page < 1 or per_page > 100:
            return jsonify({'error': 'Per page must be between 1 and 100'}), 400
        
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
        bp.add_url_rule('/bookings/tasks/<int:task_id>', 'get_booking_task_status', self.get_booking_task_status, methods=['GET'])
        bp.add_url_rule('/bookings', 'get_all_bookings', self.get_all_bookings, methods=['GET'])
        bp.add_url_rule('/bookings/<int:booking_id>', 'get_booking', self.get_booking, methods=['GET'])
        bp.add_url_rule('/users/<int:user_id>/bookings', 'get_user_bookings', self.get_user_bookings, methods=['GET'])
        bp.add_url_rule('/bookings/<int:booking_id>', 'delete_booking', self.delete_booking, methods=['DELETE'])

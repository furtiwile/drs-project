from flask import Blueprint, request, jsonify
from typing import Optional
from ..domain.dtos.rating_dto import (
    RatingCreateDTO,
    RatingUpdateDTO,
    RatingResponseDTO
)
from app.domain.interfaces.services.rating_service_interface import RatingServiceInterface
from app.domain.interfaces.controllers.rating_controller_interface import RatingControllerInterface
from .validators.rating_validator import validate_create_rating_data, validate_update_rating_data
from dataclasses import asdict

rating_bp = Blueprint('rating', __name__)


class RatingController(RatingControllerInterface):
    def __init__(self, rating_service: RatingServiceInterface, blueprint: Blueprint):
        self.rating_service = rating_service
        self.register_routes(blueprint)

    def create_rating(self):
        """
        POST /ratings
        Creates a new rating.

        Request JSON format:
        {
            "flight_id": "integer (required, min 1)",
            "rating": "integer (required, 1-5)"
        }

        Headers:
            user-id: "integer (required)"

        Returns:
            tuple: JSON response with rating data or error message, and HTTP status code.
        """
        data = request.get_json()
        
        user_id_str = request.headers.get('user-id')
        if not user_id_str:
            return jsonify({'error': 'user-id header is required'}), 400
        try:
            user_id = int(user_id_str)
        except ValueError:
            return jsonify({'error': 'Invalid user-id in header'}), 400

        try:
            validated_data: RatingCreateDTO = validate_create_rating_data(data, user_id)
        except ValueError as e:
            return jsonify(e.args[0]), 400

        rating = self.rating_service.create_rating(user_id, validated_data)
        if not rating:
            return jsonify({'error': 'Failed to create rating. Check if flight exists, has completed, and you have a booking for it.'}), 400

        response_dto = RatingResponseDTO()
        return jsonify(response_dto.dump(rating)), 201

    def update_rating(self, rating_id: int):
        """
        PUT /ratings/<int:rating_id>
        Updates an existing rating.

        Request JSON format:
        {
            "rating": "integer (required, 1-5)"
        }

        Headers:
            user-id: "integer (required)"

        Returns:
            tuple: JSON response with updated rating data or error message, and HTTP status code.
        """
        data = request.get_json()
        try:
            validated_data: RatingUpdateDTO = validate_update_rating_data(data)
        except ValueError as e:
            return jsonify(e.args[0]), 400

        user_id_str = request.headers.get('user-id')
        if not user_id_str:
            return jsonify({'error': 'user-id header is required'}), 400
        try:
            user_id = int(user_id_str)
        except ValueError:
            return jsonify({'error': 'Invalid user-id in header'}), 400

        rating = self.rating_service.update_rating(rating_id, user_id, validated_data)
        if not rating:
            return jsonify({'error': 'Failed to update rating. Check if rating exists and belongs to you.'}), 400

        response_dto = RatingResponseDTO()
        return jsonify(response_dto.dump(rating)), 200

    def get_rating(self, rating_id: int):
        """
        GET /ratings/<int:rating_id>
        Retrieves a rating by ID.

        Args:
            rating_id (int): The rating ID from the URL.

        Returns:
            tuple: JSON response with rating data or error message, and HTTP status code.
        """
        rating = self.rating_service.get_rating(rating_id)
        if not rating:
            return jsonify({'error': 'Rating not found'}), 404

        response_dto = RatingResponseDTO()
        return jsonify(response_dto.dump(rating))

    def get_user_ratings(self, user_id: int):
        """
        GET /users/<int:user_id>/ratings
        Retrieves all ratings for a user with pagination.

        Args:
            user_id (int): The user ID from the URL.

        Query parameters:
            page (int): Page number (default: 1)
            per_page (int): Items per page (default: 10)

        Returns:
            Response: JSON response with paginated list of user ratings.
        """
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)

        result = self.rating_service.get_user_ratings(user_id, page, per_page)
        response_dto = RatingResponseDTO(many=True)

        return jsonify({
            'ratings': response_dto.dump(result['ratings']),
            'page': result['page'],
            'per_page': result['per_page'],
            'total': result['total'],
            'pages': result['pages']
        })

    def get_all_ratings(self):
        """
        GET /ratings
        Retrieves all ratings with pagination.

        Query parameters:
            page (int): Page number (default: 1)
            per_page (int): Items per page (default: 10)

        Returns:
            Response: JSON response with paginated list of all ratings.
        """
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)

        result = self.rating_service.get_all_ratings(page, per_page)
        response_dto = RatingResponseDTO(many=True)

        return jsonify({
            'ratings': response_dto.dump(result['ratings']),
            'page': result['page'],
            'per_page': result['per_page'],
            'total': result['total'],
            'pages': result['pages']
        })

    def delete_rating(self, rating_id: int):
        """
        DELETE /ratings/<int:rating_id>
        Deletes a rating by ID.

        Args:
            rating_id (int): The rating ID from the URL.

        Returns:
            tuple: JSON response with success message or error message, and HTTP status code.
        """
        success = self.rating_service.delete_rating(rating_id)
        if not success:
            return jsonify({'error': 'Rating not found'}), 404

        return jsonify({'message': 'Rating deleted'}), 200

    def register_routes(self, bp: Blueprint):
        """Register routes to the blueprint."""
        bp.add_url_rule('/ratings', 'create_rating', self.create_rating, methods=['POST'])
        bp.add_url_rule('/ratings/<int:rating_id>', 'update_rating', self.update_rating, methods=['PUT'])
        bp.add_url_rule('/ratings', 'get_all_ratings', self.get_all_ratings, methods=['GET'])
        bp.add_url_rule('/ratings/<int:rating_id>', 'get_rating', self.get_rating, methods=['GET'])
        bp.add_url_rule('/users/<int:user_id>/ratings', 'get_user_ratings', self.get_user_ratings, methods=['GET'])
        bp.add_url_rule('/ratings/<int:rating_id>', 'delete_rating', self.delete_rating, methods=['DELETE'])
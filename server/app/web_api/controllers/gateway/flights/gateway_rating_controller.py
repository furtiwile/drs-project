from flask import Blueprint, Response, g, request

from app.domain.services.gateway.flights.igateway_rating_service import IGatewayRatingService
from app.domain.dtos.gateway.flights.rating.rating_create_dto import RatingCreateDTO
from app.domain.dtos.gateway.flights.rating.rating_update_dto import RatingUpdateDTO

from app.middlewares.json.json_middleware import require_json
from app.middlewares.authentication.authentication import authenticate

from app.web_api.utils.http.response_handlers import handle_response

class GatewayRatingController:
    def __init__(self, gateway_rating_service: IGatewayRatingService) -> None:
        self._gateway_rating_blueprint = Blueprint('ratings', __name__, url_prefix='/api/v1')
        self.gateway_rating_service = gateway_rating_service
        self._register_routes()
    
    def _register_routes(self) -> None:
        self._gateway_rating_blueprint.add_url_rule('/ratings', view_func=self.create_rating, methods=['POST'])
        self._gateway_rating_blueprint.add_url_rule('/ratings', view_func=self.get_all_ratings, methods=['GET'])
        self._gateway_rating_blueprint.add_url_rule('/ratings/<int:rating_id>', view_func=self.get_rating, methods=['GET'])
        self._gateway_rating_blueprint.add_url_rule('/users/ratings', view_func=self.get_user_ratings, methods=['GET'])
        self._gateway_rating_blueprint.add_url_rule('/ratings/<int:rating_id>', view_func=self.update_rating, methods=['PUT'])
        self._gateway_rating_blueprint.add_url_rule('/ratings/<int:rating_id>', view_func=self.delete_rating, methods=['DELETE'])

    @require_json
    @authenticate
    def create_rating(self) -> tuple[Response, int]:
        data = request.get_json()
        create_rating_dto = RatingCreateDTO.from_dict(data)
        created_by = g.user.user_id

        result = self.gateway_rating_service.create_rating(create_rating_dto, created_by)
        return handle_response(result, success_code=201)
    
    @authenticate
    def get_all_ratings(self) -> tuple[Response, int]:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)

        result = self.gateway_rating_service.get_all_ratings(page, per_page)
        return handle_response(result)

    @authenticate
    def get_user_ratings(self) -> tuple[Response, int]:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        user_id = g.user.user_id

        result = self.gateway_rating_service.get_user_ratings(page, per_page, user_id)
        return handle_response(result)

    @authenticate
    def get_rating(self, rating_id: int) -> tuple[Response, int]:
        result = self.gateway_rating_service.get_rating(rating_id)
        return handle_response(result)
    
    @require_json
    @authenticate
    def update_rating(self, rating_id: int) -> tuple[Response, int]:
        data = request.get_json()
        update_rating_dto = RatingUpdateDTO.from_dict(data)
        updated_by = g.user.user_id

        result = self.gateway_rating_service.update_rating(rating_id, update_rating_dto, updated_by)
        return handle_response(result)
    
    @authenticate
    def delete_rating(self, rating_id: int) -> tuple[Response, int]:
        deleted_by = g.user.user_id

        result = self.gateway_rating_service.delete_rating(rating_id, deleted_by)
        return handle_response(result, success_code=204)

    @property
    def blueprint(self) -> Blueprint:
        return self._gateway_rating_blueprint
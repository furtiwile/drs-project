from flask import Blueprint, Response, g, request

from app.domain.dtos.gateway.flights.booking.booking_create_dto import BookingCreateDTO
from app.domain.services.gateway.flights.igateway_booking_service import IGatewayBookingService

from app.middlewares.json.json_middleware import require_json
from app.middlewares.authentication.authentication import authenticate

from app.web_api.utils.http.response_handlers import handle_response

class GatewayBookingController:
    def __init__(self, gateway_booking_service: IGatewayBookingService) -> None:
        self._gateway_booking_blueprint = Blueprint('bookings', __name__, url_prefix='/api/v1')
        self.gateway_booking_service = gateway_booking_service
        self._register_routes()
    
    def _register_routes(self) -> None:
        self._gateway_booking_blueprint.add_url_rule('/bookings', view_func=self.create_booking, methods=['POST'])
        self._gateway_booking_blueprint.add_url_rule('/bookings', view_func=self.get_all_bookings, methods=['GET'])
        self._gateway_booking_blueprint.add_url_rule('/bookings/<int:booking_id>', view_func=self.get_booking, methods=['GET'])
        self._gateway_booking_blueprint.add_url_rule('/users/bookings', view_func=self.get_user_bookings, methods=['GET'])
        self._gateway_booking_blueprint.add_url_rule('/bookings/<int:booking_id>', view_func=self.delete_booking, methods=['DELETE'])

    @require_json
    @authenticate
    def create_booking(self) -> tuple[Response, int]:
        data = request.get_json()
        create_booking_dto = BookingCreateDTO.from_dict(data)
        created_by = g.user.user_id

        result = self.gateway_booking_service.create_booking(create_booking_dto, created_by)
        return handle_response(result, success_code=201)
    
    @authenticate
    def get_all_bookings(self) -> tuple[Response, int]:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)

        result = self.gateway_booking_service.get_all_bookings(page, per_page)
        return handle_response(result)

    @authenticate
    def get_booking(self, booking_id: int) -> tuple[Response, int]:
        result = self.gateway_booking_service.get_booking(booking_id)
        return handle_response(result)

    @authenticate
    def get_user_bookings(self) -> tuple[Response, int]:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        user_id = g.user.user_id

        result = self.gateway_booking_service.get_user_bookings(page, per_page, user_id)
        return handle_response(result)
    
    @authenticate
    def delete_booking(self, booking_id: int) -> tuple[Response, int]:
        deleted_by = g.user.user_id

        result = self.gateway_booking_service.delete_booking(booking_id, deleted_by)
        return handle_response(result, success_code=204)

    @property
    def blueprint(self) -> Blueprint:
        return self._gateway_booking_blueprint
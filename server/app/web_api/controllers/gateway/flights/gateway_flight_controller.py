from flask import Blueprint, Response, g, request, jsonify

from app.domain.services.gateway.flights.igateway_flight_service import IGatewayFlightService
from app.domain.dtos.gateway.flights.flight.flight_create_dto import FlightCreateDTO
from app.domain.dtos.gateway.flights.flight.flight_status_update_dto import FlightStatusUpdateDTO
from app.domain.dtos.gateway.flights.flight.flight_update_dto import FlightUpdateDTO
from app.domain.dtos.gateway.flights.flight.flight_cancel_dto import FlightCancelDTO
from app.domain.enums.role import Role

from app.middlewares.json.json_middleware import require_json
from app.middlewares.authentication.authentication import authenticate
from app.middlewares.authorization.authorization import authorize

from app.web_api.utils.http.response_handlers import handle_response

class GatewayFlightController:
    def __init__(self, gateway_flight_service: IGatewayFlightService) -> None:
        self._gateway_flight_blueprint = Blueprint('flights', __name__, url_prefix='/api/v1')
        self.gateway_flight_service = gateway_flight_service
        self._register_routes()
    
    def _register_routes(self) -> None:
        self._gateway_flight_blueprint.add_url_rule('/flights', view_func=self._handle_create_flight, methods=['POST', 'OPTIONS'])
        self._gateway_flight_blueprint.add_url_rule('/flights', view_func=self._handle_get_all_flights, methods=['GET', 'OPTIONS'])
        self._gateway_flight_blueprint.add_url_rule('/flights/tabs/<string:tab>', view_func=self._handle_get_flights_by_tab, methods=['GET', 'OPTIONS'])
        self._gateway_flight_blueprint.add_url_rule('/flights/<int:flight_id>', view_func=self._handle_get_flight, methods=['GET', 'OPTIONS'])
        self._gateway_flight_blueprint.add_url_rule('/flights/<int:flight_id>', view_func=self._handle_update_flight, methods=['PATCH', 'OPTIONS'])
        self._gateway_flight_blueprint.add_url_rule('/flights/<int:flight_id>/status', view_func=self._handle_update_flight_status, methods=['PATCH', 'OPTIONS'])
        self._gateway_flight_blueprint.add_url_rule('/flights/<int:flight_id>/cancel', view_func=self._handle_cancel_flight, methods=['POST', 'OPTIONS'])
        self._gateway_flight_blueprint.add_url_rule('/flights/<int:flight_id>', view_func=self._handle_delete_flight, methods=['DELETE', 'OPTIONS'])
        self._gateway_flight_blueprint.add_url_rule('/flights/<int:flight_id>/available-seats', view_func=self._handle_get_available_seats, methods=['GET', 'OPTIONS'])
        self._gateway_flight_blueprint.add_url_rule('/flights/<int:flight_id>/remaining-time', view_func=self._handle_get_flight_remaining_time, methods=['GET', 'OPTIONS'])
    
    def _handle_options(self, method):
        if request.method == 'OPTIONS':
            return jsonify({}), 200
        return method()
    
    def _handle_create_flight(self):
        if request.method == 'OPTIONS':
            return jsonify({}), 200
        return self.create_flight()

    def _handle_get_all_flights(self):
        if request.method == 'OPTIONS':
            return jsonify({}), 200
        return self.get_all_flights()

    def _handle_get_flights_by_tab(self, tab: str):
        if request.method == 'OPTIONS':
            return jsonify({}), 200
        return self.get_flights_by_tab(tab)

    def _handle_get_flight(self, flight_id: int):
        if request.method == 'OPTIONS':
            return jsonify({}), 200
        return self.get_flight(flight_id)

    def _handle_update_flight(self, flight_id: int):
        if request.method == 'OPTIONS':
            return jsonify({}), 200
        return self.update_flight(flight_id)

    def _handle_update_flight_status(self, flight_id: int):
        if request.method == 'OPTIONS':
            return jsonify({}), 200
        return self.update_flight_status(flight_id)

    def _handle_cancel_flight(self, flight_id: int):
        if request.method == 'OPTIONS':
            return jsonify({}), 200
        return self.cancel_flight(flight_id)

    def _handle_delete_flight(self, flight_id: int):
        if request.method == 'OPTIONS':
            return jsonify({}), 200
        return self.delete_flight(flight_id)

    def _handle_get_available_seats(self, flight_id: int):
        if request.method == 'OPTIONS':
            return jsonify({}), 200
        return self.get_available_seats(flight_id)

    def _handle_get_flight_remaining_time(self, flight_id: int):
        if request.method == 'OPTIONS':
            return jsonify({}), 200
        return self.get_flight_remaining_time(flight_id)

    @require_json
    @authenticate
    @authorize(Role.MANAGER)
    def create_flight(self) -> tuple[Response, int]:
        data = request.get_json()
        create_flight_dto = FlightCreateDTO.from_dict(data)
        created_by = g.user.user_id

        result = self.gateway_flight_service.create_flight(create_flight_dto, created_by)
        return handle_response(result, success_code=201)

    @authenticate
    def get_all_flights(self) -> tuple[Response, int]:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)

        filters = {
            k: v
            for k, v in request.args.items()
            if k not in ('page', 'per_page') and v != ""
        }

        result = self.gateway_flight_service.get_all_flights(page, per_page, filters)
        return handle_response(result)
    
    @authenticate
    def get_flights_by_tab(self, tab: str) -> tuple[Response, int]:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)

        filters = {
            k: v
            for k, v in request.args.items()
            if k not in ('page', 'per_page') and v != ""
        }

        result = self.gateway_flight_service.get_flights_by_tab(tab, page, per_page, filters)
        return handle_response(result)
    
    @authenticate
    def get_flight(self, flight_id: int) -> tuple[Response, int]:
        result = self.gateway_flight_service.get_flight(flight_id)
        return handle_response(result)
    
    @require_json
    @authenticate
    @authorize(Role.ADMINISTRATOR, Role.MANAGER)
    def update_flight(self, flight_id: int) -> tuple[Response, int]:
        data = request.get_json()
        update_flight_dto = FlightUpdateDTO.from_dict(data)
        updated_by = g.user.user_id

        result = self.gateway_flight_service.update_flight(flight_id, update_flight_dto, updated_by)
        return handle_response(result)
    
    @require_json
    @authenticate
    @authorize(Role.ADMINISTRATOR)
    def update_flight_status(self, flight_id: int) -> tuple[Response, int]:
        data = request.get_json()
        status_update_flight_dto = FlightStatusUpdateDTO.from_dict(data)
        admin_id = g.user.user_id

        result = self.gateway_flight_service.update_flight_status(flight_id, status_update_flight_dto, admin_id)
        return handle_response(result)

    @require_json
    @authenticate
    @authorize(Role.ADMINISTRATOR)
    def cancel_flight(self, flight_id: int) -> tuple[Response, int]:
        data = request.get_json()
        cancel_flight_dto = FlightCancelDTO.from_dict(data)
        admin_id = g.user.user_id

        result = self.gateway_flight_service.cancel_flight(flight_id, cancel_flight_dto, admin_id)
        return handle_response(result, success_code=204)
    
    @authenticate
    @authorize(Role.ADMINISTRATOR)
    def delete_flight(self, flight_id: int) -> tuple[Response, int]:
        admin_id = g.user.user_id

        result = self.gateway_flight_service.delete_flight(flight_id, admin_id)
        return handle_response(result, success_code=204)
    
    @authenticate
    def get_available_seats(self, flight_id: int) -> tuple[Response, int]:
        result = self.gateway_flight_service.get_available_seats(flight_id)
        return handle_response(result)

    @authenticate
    def get_flight_remaining_time(self, flight_id: int) -> tuple[Response, int]:
        result = self.gateway_flight_service.get_flight_remaining_time(flight_id)
        return handle_response(result)

    @property
    def blueprint(self) -> Blueprint:
        return self._gateway_flight_blueprint
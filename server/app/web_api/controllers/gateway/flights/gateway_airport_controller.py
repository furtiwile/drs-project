from flask import Blueprint, Response, request, jsonify

from app.domain.services.gateway.flights.igateway_airport_service import IGatewayAirportService
from app.domain.dtos.gateway.flights.airport.airport_create_dto import AirportCreateDTO
from app.domain.dtos.gateway.flights.airport.airport_update_dto import AirportUpdateDTO
from app.domain.enums.role import Role

from app.middlewares.json.json_middleware import require_json
from app.middlewares.authentication.authentication import authenticate
from app.middlewares.authorization.authorization import authorize

from app.web_api.utils.http.response_handlers import handle_response

class GatewayAirportController:
    def __init__(self, gateway_airport_service: IGatewayAirportService) -> None:
        self._gateway_airport_blueprint = Blueprint('airports', __name__, url_prefix='/api/v1')
        self.gateway_airport_service = gateway_airport_service
        self._register_routes()
    
    def _register_routes(self) -> None:
        self._gateway_airport_blueprint.add_url_rule('/airports', view_func=self._handle_create_airport, methods=['POST', 'OPTIONS'])
        self._gateway_airport_blueprint.add_url_rule('/airports', view_func=self._handle_get_all_airports, methods=['GET', 'OPTIONS'])
        self._gateway_airport_blueprint.add_url_rule('/airports/<int:airport_id>', view_func=self._handle_get_airport, methods=['GET', 'OPTIONS'])
        self._gateway_airport_blueprint.add_url_rule('/airports/<int:airport_id>', view_func=self._handle_update_airport, methods=['PATCH', 'OPTIONS'])
        self._gateway_airport_blueprint.add_url_rule('/airports/<int:airport_id>', view_func=self._handle_delete_airport, methods=['DELETE', 'OPTIONS'])
        self._gateway_airport_blueprint.add_url_rule('/airports/info/<string:airport_code>', view_func=self._handle_get_airport_info, methods=['GET', 'OPTIONS'])

    def _handle_create_airport(self):
        if request.method == 'OPTIONS':
            return jsonify({}), 200
        return self.create_airport()

    def _handle_get_all_airports(self):
        if request.method == 'OPTIONS':
            return jsonify({}), 200
        return self.get_all_airports()

    def _handle_get_airport(self, airport_id: int):
        if request.method == 'OPTIONS':
            return jsonify({}), 200
        return self.get_airport(airport_id)

    def _handle_update_airport(self, airport_id: int):
        if request.method == 'OPTIONS':
            return jsonify({}), 200
        return self.update_airport(airport_id)

    def _handle_delete_airport(self, airport_id: int):
        if request.method == 'OPTIONS':
            return jsonify({}), 200
        return self.delete_airport(airport_id)

    def _handle_get_airport_info(self, airport_code: str):
        if request.method == 'OPTIONS':
            return jsonify({}), 200
        return self.get_airport_info(airport_code)

    @require_json
    @authenticate
    @authorize(Role.ADMINISTRATOR, Role.MANAGER)
    def create_airport(self) -> tuple[Response, int]:
        data = request.get_json()
        create_airport_dto = AirportCreateDTO.from_dict(data)

        result = self.gateway_airport_service.create_airport(create_airport_dto)
        return handle_response(result, success_code=201)

    @authenticate
    def get_all_airports(self) -> tuple[Response, int]:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)

        result = self.gateway_airport_service.get_all_airports(page, per_page)
        return handle_response(result)

    @authenticate
    def get_airport(self, airport_id: int) -> tuple[Response, int]:
        result = self.gateway_airport_service.get_airport(airport_id)
        return handle_response(result)
    
    @require_json
    @authenticate
    @authorize(Role.ADMINISTRATOR, Role.MANAGER)
    def update_airport(self, airport_id: int) -> tuple[Response, int]:
        data = request.get_json()
        update_airport_dto = AirportUpdateDTO.from_dict(data)

        result = self.gateway_airport_service.update_airport(airport_id, update_airport_dto)
        return handle_response(result)

    @authenticate
    @authorize(Role.ADMINISTRATOR, Role.MANAGER)
    def delete_airport(self, airport_id: int) -> tuple[Response, int]:
        result = self.gateway_airport_service.delete_airport(airport_id)
        return handle_response(result, success_code=204)

    @authenticate
    def get_airport_info(self, airport_code: str) -> tuple[Response, int]:
        result = self.gateway_airport_service.get_airport_info(airport_code)
        return handle_response(result)
        
    @property
    def blueprint(self) -> Blueprint:
        return self._gateway_airport_blueprint
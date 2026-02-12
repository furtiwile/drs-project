from flask import Blueprint, Response, request, jsonify

from app.domain.dtos.gateway.flights.airline.airline_update_dto import AirlineUpdateDTO
from app.domain.services.gateway.flights.igateway_airline_service import IGatewayAirlineService
from app.domain.dtos.gateway.flights.airline.airline_create_dto import AirlineCreateDTO
from app.domain.enums.role import Role

from app.middlewares.json.json_middleware import require_json
from app.middlewares.authentication.authentication import authenticate
from app.middlewares.authorization.authorization import authorize

from app.web_api.controllers.auth.auth_controller import handle_response

class GatewayAirlineController:
    def __init__(self, gateway_airline_service: IGatewayAirlineService) -> None:
        self._gateway_airline_blueprint = Blueprint('airlines', __name__, url_prefix='/api/v1')
        self.gateway_airline_service = gateway_airline_service
        self._register_routes()
    
    def _register_routes(self) -> None:
        self._gateway_airline_blueprint.add_url_rule('/airlines', view_func=self._handle_create_airline, methods=['POST', 'OPTIONS'])
        self._gateway_airline_blueprint.add_url_rule('/airlines', view_func=self._handle_get_all_airlines, methods=['GET', 'OPTIONS'])
        self._gateway_airline_blueprint.add_url_rule('/airlines/<int:airline_id>', view_func=self._handle_get_airline, methods=['GET', 'OPTIONS'])
        self._gateway_airline_blueprint.add_url_rule('/airlines/<int:airline_id>', view_func=self._handle_update_airline, methods=['PATCH', 'OPTIONS'])
        self._gateway_airline_blueprint.add_url_rule('/airlines/<int:airline_id>', view_func=self._handle_delete_airline, methods=['DELETE', 'OPTIONS'])

    def _handle_create_airline(self):
        if request.method == 'OPTIONS':
            return jsonify({}), 200
        return self.create_airline()

    def _handle_get_all_airlines(self):
        if request.method == 'OPTIONS':
            return jsonify({}), 200
        return self.get_all_airlines()

    def _handle_get_airline(self, airline_id: int):
        if request.method == 'OPTIONS':
            return jsonify({}), 200
        return self.get_airline(airline_id)

    def _handle_update_airline(self, airline_id: int):
        if request.method == 'OPTIONS':
            return jsonify({}), 200
        return self.update_airline(airline_id)

    def _handle_delete_airline(self, airline_id: int):
        if request.method == 'OPTIONS':
            return jsonify({}), 200
        return self.delete_airline(airline_id)

    @require_json
    @authenticate
    @authorize(Role.ADMINISTRATOR, Role.MANAGER)
    def create_airline(self) -> tuple[Response, int]:
        data = request.get_json()
        create_airline_dto = AirlineCreateDTO.from_dict(data)

        result = self.gateway_airline_service.create_airline(create_airline_dto)
        return handle_response(result, success_code=201)
    
    @authenticate
    def get_all_airlines(self) -> tuple[Response, int]:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)

        result = self.gateway_airline_service.get_all_airlines(page, per_page)
        return handle_response(result)

    @authenticate
    def get_airline(self, airline_id: int) -> tuple[Response, int]:
        result = self.gateway_airline_service.get_airline(airline_id)
        return handle_response(result)
    
    @require_json
    @authenticate
    @authorize(Role.ADMINISTRATOR, Role.MANAGER)
    def update_airline(self, airline_id: int) -> tuple[Response, int]:
        data = request.get_json()
        update_airline_dto = AirlineUpdateDTO.from_dict(data)

        result = self.gateway_airline_service.update_airline(airline_id, update_airline_dto)
        return handle_response(result)
    
    @authenticate
    @authorize(Role.ADMINISTRATOR, Role.MANAGER)
    def delete_airline(self, airline_id: int) -> tuple[Response, int]:
        result = self.gateway_airline_service.delete_airline(airline_id)
        return handle_response(result, success_code=204)

    @property
    def blueprint(self) -> Blueprint:
        return self._gateway_airline_blueprint
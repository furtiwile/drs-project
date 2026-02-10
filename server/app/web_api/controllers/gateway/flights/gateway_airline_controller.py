from flask import Blueprint, Response, jsonify, request
from app.middlewares.authentication.authentication import authenticate
from app.middlewares.authorization.authorization import authorize
from app.domain.enums.role import Role
from app.middlewares.json.json_middleware import require_json
from app.domain.types.gateway_result import ok
from app.domain.dtos.gateway.flights.airline.airline_update_dto import AirlineUpdateDTO
from app.domain.services.gateway.flights.igateway_airline_service import IGatewayAirlineService
from app.domain.dtos.gateway.flights.airline.airline_create_dto import AirlineCreateDTO

class GatewayAirlineController:
    def __init__(self, gateway_airline_service: IGatewayAirlineService) -> None:
        self._gateway_airline_blueprint = Blueprint('airlines', __name__, url_prefix='/api/v1/flights')
        self.gateway_airline_service = gateway_airline_service
        self._register_routes()
    
    def _register_routes(self) -> None:
        self._gateway_airline_blueprint.add_url_rule('/airlines', view_func=self.create_airline, methods=['POST'])
        self._gateway_airline_blueprint.add_url_rule('/airlines', view_func=self.get_all_airlines, methods=['GET'])
        self._gateway_airline_blueprint.add_url_rule('/airlines/<int:airline_id>', view_func=self.get_airline, methods=['GET'])
        self._gateway_airline_blueprint.add_url_rule('/airlines/<int:airline_id>', view_func=self.update_airline, methods=['PATCH'])
        self._gateway_airline_blueprint.add_url_rule('/airlines/<int:airline_id>', view_func=self.delete_airline, methods=['DELETE'])

    @require_json
    @authenticate
    @authorize(Role.MANAGER)
    def create_airline(self) -> tuple[Response, int]:
        data = request.get_json()
        create_airline_dto = AirlineCreateDTO.from_dict(data)

        result = self.gateway_airline_service.create_airline(create_airline_dto)
        if isinstance(result, ok):
            return jsonify(result.data), 201
        else:
            return jsonify(message=result.message), result.status_code
    
    @authenticate
    @authorize(Role.MANAGER)
    def get_all_airlines(self) -> tuple[Response, int]:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)

        result = self.gateway_airline_service.get_all_airlines(page, per_page)
        if isinstance(result, ok):
            return jsonify(result.data), 200
        else:
            return jsonify(message=result.message), result.status_code

    @authenticate
    @authorize(Role.MANAGER)
    def get_airline(self, airline_id: int) -> tuple[Response, int]:
        result = self.gateway_airline_service.get_airline(airline_id)
        if isinstance(result, ok):
            return jsonify(result.data), 200
        else:
            return jsonify(message=result.message), result.status_code
    
    @require_json
    @authenticate
    @authorize(Role.MANAGER)
    def update_airline(self, airline_id: int) -> tuple[Response, int]:
        data = request.get_json()
        update_airline_dto = AirlineUpdateDTO.from_dict(data)

        result = self.gateway_airline_service.update_airline(airline_id, update_airline_dto)
        if isinstance(result, ok):
            return jsonify(result.data), 200
        else:
            return jsonify(message=result.message), result.status_code
    
    @authenticate
    @authorize(Role.MANAGER)
    def delete_airline(self, airline_id: int) -> tuple[Response, int]:
        result = self.gateway_airline_service.delete_airline(airline_id)
        if isinstance(result, ok):
            return jsonify(None), 204
        else:
            return jsonify(message=result.message), result.status_code

    @property
    def blueprint(self) -> Blueprint:
        return self._gateway_airline_blueprint
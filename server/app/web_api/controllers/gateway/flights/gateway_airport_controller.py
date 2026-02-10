from flask import Blueprint, Response, jsonify, request
from app.domain.services.gateway.flights.igateway_airport_service import IGatewayAirportService
from app.middlewares.json.json_middleware import require_json
from app.middlewares.authentication.authentication import authenticate
from app.domain.enums.role import Role
from app.middlewares.authorization.authorization import authorize
from app.domain.dtos.gateway.flights.airport.airport_create_dto import AirportCreateDTO
from app.domain.types.gateway_result import ok
from app.domain.dtos.gateway.flights.airport.airport_update_dto import AirportUpdateDTO

class GatewayAirportController:
    def __init__(self, gateway_airport_service: IGatewayAirportService) -> None:
        self._gateway_airport_blueprint = Blueprint('airports', __name__, url_prefix='/api/v1')
        self.gateway_airport_service = gateway_airport_service
        self._register_routes()
    
    def _register_routes(self) -> None:
        self._gateway_airport_blueprint.add_url_rule('/airports', view_func=self.create_airport, methods=['POST'])
        self._gateway_airport_blueprint.add_url_rule('/airports', view_func=self.get_all_airports, methods=['GET'])
        self._gateway_airport_blueprint.add_url_rule('/airports/<int:airport_id>', view_func=self.get_airport, methods=['GET'])
        self._gateway_airport_blueprint.add_url_rule('/airports/<int:airport_id>', view_func=self.update_airport, methods=['PATCH'])
        self._gateway_airport_blueprint.add_url_rule('/airports/<int:airport_id>', view_func=self.delete_airport, methods=['DELETE'])
        self._gateway_airport_blueprint.add_url_rule('/airports/info/<airport_code>', view_func=self.get_airport_info, methods=['GET'])

    @require_json
    @authenticate
    @authorize(Role.ADMINISTRATOR, Role.MANAGER)
    def create_airport(self) -> tuple[Response, int]:
        data = request.get_json()
        create_airport_dto = AirportCreateDTO.from_dict(data)

        result = self.gateway_airport_service.create_airport(create_airport_dto)
        if isinstance(result, ok):
            return jsonify(result.data), 201
        else:
            return jsonify(message=result.message), result.status_code

    @authenticate
    def get_all_airports(self) -> tuple[Response, int]:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)

        result = self.gateway_airport_service.get_all_airports(page, per_page)
        if isinstance(result, ok):
            return jsonify(result.data), 200
        else:
            return jsonify(message=result.message), result.status_code

    @authenticate
    def get_airport(self, airport_id: int) -> tuple[Response, int]:
        result = self.gateway_airport_service.get_airport(airport_id)
        if isinstance(result, ok):
            return jsonify(result.data), 200
        else:
            return jsonify(message=result.message), result.status_code
    
    @require_json
    @authenticate
    @authorize(Role.ADMINISTRATOR, Role.MANAGER)
    def update_airport(self, airport_id: int) -> tuple[Response, int]:
        data = request.get_json()
        update_airport_dto = AirportUpdateDTO.from_dict(data)

        result = self.gateway_airport_service.update_airport(airport_id, update_airport_dto)
        if isinstance(result, ok):
            return jsonify(result.data), 200
        else:
            return jsonify(message=result.message), result.status_code

    @authenticate
    @authorize(Role.ADMINISTRATOR, Role.MANAGER)
    def delete_airport(self, airport_id: int) -> tuple[Response, int]:
        result = self.gateway_airport_service.delete_airport(airport_id)
        if isinstance(result, ok):
            return jsonify(None), 204
        else:
            return jsonify(message=result.message), result.status_code

    @authenticate
    def get_airport_info(self, airport_code: str) -> tuple[Response, int]:
        result = self.gateway_airport_service.get_airport_info(airport_code)
        if isinstance(result, ok):
            return jsonify(result.data), 200
        else:
            return jsonify(message=result.message), result.status_code
        
    @property
    def blueprint(self) -> Blueprint:
        return self._gateway_airport_blueprint
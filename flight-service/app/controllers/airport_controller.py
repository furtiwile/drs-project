from flask import Blueprint, request, jsonify
from typing import Optional
from ..domain.dtos.airport_dto import AirportCreateDTO, AirportUpdateDTO, AirportResponseDTO
from ..services.interfaces import AirportServiceInterface
from .interfaces import AirportControllerInterface

airport_bp = Blueprint('airport', __name__)

class AirportController(AirportControllerInterface):
    def __init__(self, airport_service: AirportServiceInterface, blueprint: Blueprint):
        self.airport_service = airport_service
        self.register_routes(blueprint)

    def create_airport(self):
        data = request.get_json()
        dto = AirportCreateDTO()
        errors = dto.validate(data)
        if errors:
            return jsonify(errors), 400
        airport = self.airport_service.create_airport(data)
        response_dto = AirportResponseDTO()
        return jsonify(response_dto.dump(airport)), 201

    def get_airport(self, airport_id: int):
        airport = self.airport_service.get_airport(airport_id)
        if not airport:
            return jsonify({'error': 'Airport not found'}), 404
        response_dto = AirportResponseDTO()
        return jsonify(response_dto.dump(airport))

    def get_all_airports(self):
        airports = self.airport_service.get_all_airports()
        response_dto = AirportResponseDTO(many=True)
        return jsonify(response_dto.dump(airports))

    def update_airport(self, airport_id: int):
        data = request.get_json()
        dto = AirportUpdateDTO()
        errors = dto.validate(data)
        if errors:
            return jsonify(errors), 400
        airport = self.airport_service.update_airport(airport_id, data)
        if not airport:
            return jsonify({'error': 'Airport not found'}), 404
        response_dto = AirportResponseDTO()
        return jsonify(response_dto.dump(airport))

    def delete_airport(self, airport_id: int):
        success = self.airport_service.delete_airport(airport_id)
        if not success:
            return jsonify({'error': 'Airport not found'}), 404
        return jsonify({'message': 'Airport deleted'}), 200

    def get_airport_info(self, airport_code: str):
        airport = self.airport_service.fetch_airport_info(airport_code)
        if not airport:
            return jsonify({'error': 'Airport not found'}), 404
        response_dto = AirportResponseDTO()
        return jsonify(response_dto.dump(airport))

    def register_routes(self, bp: Blueprint):
        bp.add_url_rule('/airports', 'create_airport', self.create_airport, methods=['POST'])
        bp.add_url_rule('/airports', 'get_all_airports', self.get_all_airports, methods=['GET'])
        bp.add_url_rule('/airports/<int:airport_id>', 'get_airport', self.get_airport, methods=['GET'])
        bp.add_url_rule('/airports/<int:airport_id>', 'update_airport', self.update_airport, methods=['PUT'])
        bp.add_url_rule('/airports/<int:airport_id>', 'delete_airport', self.delete_airport, methods=['DELETE'])
        bp.add_url_rule('/airports/info/<airport_code>', 'get_airport_info', self.get_airport_info, methods=['GET'])
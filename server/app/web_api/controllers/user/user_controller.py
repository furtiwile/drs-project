from flask import Blueprint, request, jsonify, g
from flask.wrappers import Response

from app.domain.services.user.iuser_service import IUserService
from app.domain.dtos.user.user_dto import UserDTO
from app.domain.dtos.user.update_user_dto import UpdateUserDTO
from app.domain.dtos.user.transaction_dto import TransactionDTO
from app.domain.dtos.user.update_role_dto import UpdateRoleDTO
from app.domain.enums.role import Role

from app.middlewares.authentication.authentication import authenticate
from app.middlewares.authorization.authorization import authorize
from app.middlewares.json.json_middleware import require_json

from app.web_api.utils.http.response_handlers import handle_response
from app.web_api.validators.user.user_validators import (
    validate_transaction, 
    validate_update_user, 
    validate_update_user_role_by_id, 
    validate_user_id
)

class UserController:
    def __init__(self, user_service: IUserService) -> None:
        self.user_service = user_service
        self._user_blueprint = Blueprint('user', __name__, url_prefix='/api/v1/users')
        self._register_routes()

    def _register_routes(self) -> None:
        self._user_blueprint.add_url_rule('/', view_func=self.get_all_users, methods=['GET'])
        self._user_blueprint.add_url_rule('/<int:user_id>', view_func=self.get_user_by_id, methods=['GET'])
        self._user_blueprint.add_url_rule('/<int:user_id>', view_func=self.update_user_role_by_id, methods=['PATCH'])
        self._user_blueprint.add_url_rule('/', view_func=self.update_user, methods=['PATCH'])
        self._user_blueprint.add_url_rule('/<int:user_id>', view_func=self.delete_user_by_id, methods=['DELETE'])
        self._user_blueprint.add_url_rule('/deposit', view_func=self.deposit, methods=['PATCH'])
        self._user_blueprint.add_url_rule('/withdraw', view_func=self.withdraw, methods=['PATCH'])
    
    @authenticate
    @authorize(Role.ADMINISTRATOR)
    def get_all_users(self) -> tuple[Response, int]:
        result = self.user_service.get_all_users()
        return handle_response(result, to_json=lambda users: [UserDTO.from_model(u).to_dict() for u in users])

    @authenticate
    def get_user_by_id(self, user_id: int) -> tuple[Response, int]:
        if not (valid_data := validate_user_id(user_id)):
            return jsonify(message=valid_data.message), 400

        result = self.user_service.get_user_by_id(user_id)
        return handle_response(result, to_json=lambda u: UserDTO.from_model(u).to_dict())

    @require_json
    @authenticate
    @authorize(Role.ADMINISTRATOR)
    def update_user_role_by_id(self, user_id: int) -> tuple[Response, int]:
        data = request.get_json()
        update_role_dto = UpdateRoleDTO.from_dict(data)
        if not (valid_data := validate_update_user_role_by_id(user_id, update_role_dto)):
            return jsonify(message=valid_data.message), 400

        result = self.user_service.update_user_role_by_id(user_id, update_role_dto)
        return handle_response(result, success_code=204)
    
    @require_json
    @authenticate
    def update_user(self) -> tuple[Response, int]:
        data = request.get_json()
        update_user_dto = UpdateUserDTO.from_dict(data)
        user_id = g.user.user_id
        if not (valid_data := validate_update_user(user_id, update_user_dto)):
            return jsonify(message=valid_data.message), 400

        result = self.user_service.update_user(user_id, update_user_dto)
        return handle_response(result, to_json=lambda u: UserDTO.from_model(u).to_dict())

    @authenticate
    @authorize(Role.ADMINISTRATOR)
    def delete_user_by_id(self, user_id: int) -> tuple[Response, int]:
        if not (valid_data := validate_user_id(user_id)):
            return jsonify(message=valid_data.message), 400
        
        result = self.user_service.delete_user_by_id(user_id)
        return handle_response(result, success_code=204)

    @require_json
    @authenticate
    def deposit(self) -> tuple[Response, int]:
        data = request.get_json()
        transaction_dto = TransactionDTO.from_dict(data)
        user_id = g.user.user_id
        if not (valid_data := validate_transaction(user_id, transaction_dto)):
            return jsonify(message=valid_data.message), 400

        result = self.user_service.deposit(user_id, transaction_dto)
        return handle_response(result, success_code=204)

    @require_json
    @authenticate
    def withdraw(self) -> tuple[Response, int]:
        data = request.get_json()
        transaction_dto = TransactionDTO.from_dict(data)
        user_id = g.user.user_id
        if not (valid_data := validate_transaction(user_id, transaction_dto)):
            return jsonify(message=valid_data.message), 400
        
        result = self.user_service.withdraw(user_id, transaction_dto)
        return handle_response(result, success_code=204)

    @property
    def blueprint(self) -> Blueprint:
        return self._user_blueprint

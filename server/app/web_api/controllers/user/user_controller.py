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
        self._user_blueprint.add_url_rule('/', view_func=self._handle_all_users, methods=['GET', 'OPTIONS'])
        self._user_blueprint.add_url_rule('/<int:user_id>', view_func=self._handle_user_by_id, methods=['GET', 'OPTIONS'])
        self._user_blueprint.add_url_rule('/<int:user_id>', view_func=self._handle_update_user_role, methods=['PATCH', 'OPTIONS'])
        self._user_blueprint.add_url_rule('/', view_func=self._handle_update_user_wrapper, methods=['PATCH', 'OPTIONS'])
        self._user_blueprint.add_url_rule('/<int:user_id>', view_func=self._handle_delete_user, methods=['DELETE', 'OPTIONS'])
        self._user_blueprint.add_url_rule('/deposit', view_func=self._handle_deposit, methods=['PATCH', 'OPTIONS'])
        self._user_blueprint.add_url_rule('/withdraw', view_func=self._handle_withdraw, methods=['PATCH', 'OPTIONS'])
    
    def _handle_method(self, method):
        """Handle CORS preflight OPTIONS request without authentication"""
        if request.method == 'OPTIONS':
            return jsonify({}), 200
        return method()
    
    def _handle_all_users(self) -> tuple[Response, int]:
        if request.method == 'OPTIONS':
            return jsonify({}), 200
        return self.get_all_users()

    def _handle_user_by_id(self, user_id: int) -> tuple[Response, int]:
        if request.method == 'OPTIONS':
            return jsonify({}), 200
        return self.get_user_by_id(user_id)

    def _handle_update_user_role(self, user_id: int) -> tuple[Response, int]:
        if request.method == 'OPTIONS':
            return jsonify({}), 200
        return self.update_user_role_by_id(user_id)
    
    def _handle_update_user_wrapper(self) -> tuple[Response, int]:
        if request.method == 'OPTIONS':
            return jsonify({}), 200
        return self.update_user()
    
    def _handle_delete_user(self, user_id: int) -> tuple[Response, int]:
        if request.method == 'OPTIONS':
            return jsonify({}), 200
        return self.delete_user_by_id(user_id)

    def _handle_deposit(self) -> tuple[Response, int]:
        if request.method == 'OPTIONS':
            return jsonify({}), 200
        return self.deposit()

    def _handle_withdraw(self) -> tuple[Response, int]:
        if request.method == 'OPTIONS':
            return jsonify({}), 200
        return self.withdraw()
    
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

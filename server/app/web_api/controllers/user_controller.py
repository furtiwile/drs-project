from flask import Blueprint, request, jsonify, g
from app.domain.services.iuser_service import IUserService
from app.domain.dtos.user.user_dto import UserDTO
from app.domain.enums.Role import Role
from app.middlewares.authentication.authentication import authenticate
from app.middlewares.authorization.authorization import authorize
from app.middlewares.json.json_middleware import require_json
from app.repositories.user_repository import UpdateUserDTO
from app.utils.converters.error_type_converter import error_type_to_http
from app.web_api.validators.user_validators import validate_update_user, validate_update_user_role_by_id, validate_user_id

class UserController:
    def __init__(self, user_service: IUserService):
        self.user_service = user_service
        self._user_blueprint = Blueprint('user', __name__, url_prefix='/api/v1/users')
        self._register_routes()

    def _register_routes(self):
        self._user_blueprint.add_url_rule('/', view_func=self.get_all_users, methods=['GET'])
        self._user_blueprint.add_url_rule('/<int:user_id>', view_func=self.get_user_by_id, methods=['GET'])
        self._user_blueprint.add_url_rule('/<int:user_id>', view_func=self.update_user_role_by_id, methods=['PATCH'])
        self._user_blueprint.add_url_rule('/', view_func=self.update_user, methods=['PATCH'])
        self._user_blueprint.add_url_rule('/<int:user_id>', view_func=self.delete_user_by_id, methods=['DELETE'])
    
    @authenticate
    @authorize(Role.ADMINISTRATOR)
    def get_all_users(self):
        result = self.user_service.get_all_users()
        if(result.success):
            return jsonify([UserDTO.from_model(user).to_dict() for user in result.data]), 200
        else:
            return jsonify(message=result.message), error_type_to_http(result.status_code)

    @authenticate
    @authorize(Role.ADMINISTRATOR)
    def get_user_by_id(self, user_id: int):
        if not (valid_data := validate_user_id(user_id)):
            return jsonify(message=valid_data.message), 400

        result = self.user_service.get_user_by_id(user_id)
        if(result.success):
            return jsonify(UserDTO.from_model(result.data).to_dict()), 200
        else:
            return jsonify(message=result.message), error_type_to_http(result.status_code)

    @require_json
    @authenticate
    @authorize(Role.ADMINISTRATOR)
    def update_user_role_by_id(self, user_id: int):
        role = request.get_json().get('role')
        if not (valid_data := validate_update_user_role_by_id(user_id, role)):
            return jsonify(message=valid_data.message), 400

        result = self.user_service.update_user_role_by_id(user_id, Role(role))
        if(result.success):
            return jsonify(None), 204
        else:
            return jsonify(message=result.message), error_type_to_http(result.status_code)
    
    @require_json
    @authenticate
    def update_user(self):
        data = request.get_json()
        update_user_dto = UpdateUserDTO.from_dict(data)
        user_id = g.user.user_id
        if not (valid_data := validate_update_user(user_id, update_user_dto)):
            return jsonify(message=valid_data.message), 400

        result = self.user_service.update_user(user_id, update_user_dto)
        if(result.success):
            return jsonify(UserDTO.from_model(result.data).to_dict()), 200
        else:
            return jsonify(message=result.message), error_type_to_http(result.status_code)

    @authenticate
    @authorize(Role.ADMINISTRATOR)
    def delete_user_by_id(self, user_id: int):
        if not (valid_data := validate_user_id(user_id)):
            return jsonify(message=valid_data.message), 400
        
        result = self.user_service.delete_user_by_id(user_id)
        if(result.success):
            return jsonify(None), 204
        else:
            return jsonify(message=result.message), error_type_to_http(result.status_code)

    @property
    def blueprint(self):
        return self._user_blueprint

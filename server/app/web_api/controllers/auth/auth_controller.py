from flask import Blueprint, jsonify, request
from flask_jwt_extended import create_access_token
from app.domain.dtos.auth.register_user_dto import RegisterUserDTO
from app.domain.dtos.user.user_dto import UserDTO
from app.domain.models.user import User
from app.domain.dtos.auth.login_user_dto import LoginUserDTO
from app.middlewares.json.json_middleware import require_json
from app.services.auth.auth_service import IAuthService
from app.utils.converters.error_type_converter import error_type_to_http
from app.web_api.validators.auth.auth_validators import validate_login, validate_registration
from app.middlewares.authentication.authentication import authenticate

class AuthController:
    def __init__(self, auth_service: IAuthService):
        self.auth_service = auth_service
        self._auth_blueprint = Blueprint('auth', __name__, url_prefix='/api/v1/auth')
        self._register_routes()

    def _register_routes(self):
        self._auth_blueprint.add_url_rule('/login', view_func=self.login, methods=['POST'])
        self._auth_blueprint.add_url_rule('/register', view_func=self.register, methods=['POST'])
        self._auth_blueprint.add_url_rule('/logout', view_func=self.logout, methods=['POST'])

    @require_json
    def login(self):
        data = request.get_json()
        login_dto = LoginUserDTO.from_dict(data)

        if not (valid_data := validate_login(login_dto)):
            return jsonify(message=valid_data.message), 400

        ip_address = request.remote_addr
        result = self.auth_service.login(login_dto, ip_address)
        if(result.success):
            user: User = result.data
            token = create_access_token(identity=str(user.user_id), additional_claims={"role": user.role.value})
            
            return jsonify({
                "token": token,
                "user": UserDTO.from_model(user).to_dict()
            }), 200
        else:
            return jsonify(message=result.message), error_type_to_http(result.status_code)

    @require_json
    def register(self):
        data = request.get_json()
        register_dto = RegisterUserDTO.from_dict(data)

        if not (valid_data := validate_registration(register_dto)):
            return jsonify(message=valid_data.message), 400

        result = self.auth_service.register(register_dto)
        if(result.success):
            user: User = result.data
            token = create_access_token(identity=str(user.user_id), additional_claims={"role": user.role.value})
            
            return jsonify({
                "token": token,
                "user": UserDTO.from_model(user).to_dict()
            }), 201
        else:
            return jsonify(message=result.message), error_type_to_http(result.status_code)

    @authenticate
    def logout(self):
        jwt_token = request.headers.get('Authorization').split(" ")[1]
       
        result = self.auth_service.logout(jwt_token)
        if(result.success):
            return jsonify(None), 204
        else:
            return jsonify(message=result.message), error_type_to_http(result.status_code)

    @property
    def blueprint(self):
        return self._auth_blueprint
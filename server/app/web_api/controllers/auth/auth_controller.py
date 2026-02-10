from typing import cast
from flask import Blueprint, jsonify, request
from flask.wrappers import Response

from app.domain.dtos.auth.login_user_dto import LoginUserDTO
from app.domain.dtos.auth.register_user_dto import RegisterUserDTO

from app.middlewares.json.json_middleware import require_json
from app.middlewares.authentication.authentication import authenticate

from app.services.auth.auth_service import IAuthService

from app.web_api.validators.auth.auth_validators import validate_login, validate_registration
from app.web_api.utils.http.response_handlers import handle_auth_response, handle_response

class AuthController:
    def __init__(self, auth_service: IAuthService) -> None:
        self.auth_service = auth_service
        self._auth_blueprint = Blueprint('auth', __name__, url_prefix='/api/v1/auth')
        self._register_routes()

    def _register_routes(self) -> None:
        self._auth_blueprint.add_url_rule('/login', view_func=self.login, methods=['POST'])
        self._auth_blueprint.add_url_rule('/register', view_func=self.register, methods=['POST'])
        self._auth_blueprint.add_url_rule('/logout', view_func=self.logout, methods=['POST'])

    @require_json
    def login(self) -> tuple[Response, int]:
        data = request.get_json()
        login_dto = LoginUserDTO.from_dict(data)

        if not (valid_data := validate_login(login_dto)):
            return jsonify(message=valid_data.message), 400

        ip_address = request.remote_addr if request.remote_addr else ""
        result = self.auth_service.login(login_dto, ip_address)
        return handle_auth_response(result)

    @require_json
    def register(self) -> tuple[Response, int]:
        data = request.get_json()
        register_dto = RegisterUserDTO.from_dict(data)

        if not (valid_data := validate_registration(register_dto)):
            return jsonify(message=valid_data.message), 400

        result = self.auth_service.register(register_dto)
        return handle_auth_response(result, 201)

    @authenticate
    def logout(self) -> tuple[Response, int]:
        jwt_token = cast(str, request.headers.get('Authorization')).split(" ")[1]
       
        result = self.auth_service.logout(jwt_token)
        return handle_response(result, success_code=204)

    @property
    def blueprint(self) -> Blueprint:
        return self._auth_blueprint
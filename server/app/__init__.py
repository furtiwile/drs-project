from dotenv import load_dotenv
load_dotenv()

import os
from datetime import timedelta
from flask import Flask
from flask_jwt_extended import JWTManager
from flask_cors import CORS

from app.database.pgsql import engine, Base
from app.database import get_redis_client, init_redis

from app.repositories.user.user_repository import UserRepository
from app.repositories.redis.blacklist_repository import BlacklistRepository
from app.repositories.redis.blocklist_repository import BlocklistRepository

from app.infrastructure.gateway.gateway_client import GatewayClient

from app.services.auth.auth_service import AuthService
from app.services.mail.mail_service import MailService
from app.services.user.user_service import UserService
from app.services.gateway.gateway_airline_service import GatewayAirlineService

from app.web_api.controllers.auth.auth_controller import AuthController
from app.web_api.controllers.user.user_controller import UserController
from app.web_api.controllers.gateway.gateway_flights_controller import GatewayFlightsController

def create_app() -> Flask:
    app = Flask(__name__)

    CORS(app, resources={r"/api/*": { "origins": os.getenv("CORS_ORIGINS", "").split(',') }}, supports_credentials=True)

    app.config['MAX_CONTENT_LENGTH'] = 10 * 1024 * 1024

    app.config['SQLALCHEMY_DATABASE_URI'] = str(engine.url)
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=1)
    app.config["JWT_ALGORITHM"] = "HS256"

    JWTManager(app)

    init_redis()

    with app.app_context():
        Base.metadata.create_all(bind=engine)

    user_repository = UserRepository()
    blacklist_repository = BlacklistRepository(get_redis_client(), ttl=3600)
    blocklist_repository = BlocklistRepository(get_redis_client(), block_threshold=3, ttl=60)

    mail_service = MailService()
    auth_service = AuthService(user_repository, blacklist_repository, blocklist_repository)
    user_service = UserService(user_repository, mail_service)

    gateway_flights_base_url = os.getenv("FLIGHTS_URL", "")
    gateway_flights_version = os.getenv("FLIGHTS_VERSION", "/api/v1")
    gateway_flights_client = GatewayClient(base_url=gateway_flights_base_url, version=gateway_flights_version)
    gateway_airline_service = GatewayAirlineService(gateway_flights_client)

    auth_controller = AuthController(auth_service)
    user_controller = UserController(user_service)
    gateway_flights_controller = GatewayFlightsController(gateway_airline_service)

    app.register_blueprint(auth_controller.blueprint)
    app.register_blueprint(user_controller.blueprint)
    app.register_blueprint(gateway_flights_controller.blueprint)

    return app

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
from app.repositories.redis.cache_repository import CacheRepository

from app.infrastructure.gateway.gateway_client import GatewayClient

from app.services.auth.auth_service import AuthService
from app.services.mail.mail_service import MailService
from app.services.user.user_service import UserService
from app.services.gateway.flights.gateway_airline_service import GatewayAirlineService
from app.services.gateway.flights.gateway_airport_service import GatewayAirportService
from app.services.gateway.flights.gateway_flight_service import GatewayFlightService
from app.services.gateway.flights.gateway_rating_service import GatewayRatingService
from app.services.gateway.flights.gateway_booking_service import GatewayBookingService
from app.services.gateway.flights.gateway_report_service import GatewayReportService

from app.web_api.controllers.auth.auth_controller import AuthController
from app.web_api.controllers.user.user_controller import UserController
from app.web_api.controllers.gateway.flights.gateway_airline_controller import GatewayAirlineController
from app.web_api.controllers.gateway.flights.gateway_airport_controller import GatewayAirportController
from app.web_api.controllers.gateway.flights.gateway_flight_controller import GatewayFlightController
from app.web_api.controllers.gateway.flights.gateway_rating_controller import GatewayRatingController
from app.web_api.controllers.gateway.flights.gateway_booking_controller import GatewayBookingController
from app.web_api.controllers.gateway.flights.gateway_report_controller import GatewayReportController

from app.web_socket.socket import socketio

def create_app() -> Flask:
    app = Flask(__name__)

    CORS(app, origins="*", supports_credentials=True)

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
    cache_repository = CacheRepository(get_redis_client())

    mail_service = MailService()
    auth_service = AuthService(user_repository, blacklist_repository, blocklist_repository)
    user_service = UserService(user_repository, mail_service, cache_repository)

    gateway_flights_base_url = os.getenv("FLIGHTS_URL", "0.0.0.0")
    gateway_flights_version = os.getenv("FLIGHTS_VERSION", "/api/v1")
    gateway_flights_client = GatewayClient(base_url=gateway_flights_base_url, version=gateway_flights_version)
    gateway_airline_service = GatewayAirlineService(gateway_flights_client, cache_repository)
    gateway_airport_service = GatewayAirportService(gateway_flights_client, cache_repository)
    gateway_flight_service = GatewayFlightService(gateway_flights_client, user_repository, mail_service, cache_repository)
    gateway_rating_service = GatewayRatingService(gateway_flights_client)
    gateway_booking_service = GatewayBookingService(gateway_flights_client, gateway_flight_service, user_repository)
    gateway_report_service = GatewayReportService(gateway_flights_client, user_repository, mail_service)

    auth_controller = AuthController(auth_service)
    user_controller = UserController(user_service)
    gateway_airline_controller = GatewayAirlineController(gateway_airline_service)
    gateway_airport_controller = GatewayAirportController(gateway_airport_service)
    gateway_flight_controller = GatewayFlightController(gateway_flight_service)
    gateway_rating_controller = GatewayRatingController(gateway_rating_service)
    gateway_booking_controller = GatewayBookingController(gateway_booking_service)
    gateway_report_controller = GatewayReportController(gateway_report_service)

    app.register_blueprint(auth_controller.blueprint)
    app.register_blueprint(user_controller.blueprint)
    app.register_blueprint(gateway_airline_controller.blueprint)
    app.register_blueprint(gateway_airport_controller.blueprint)
    app.register_blueprint(gateway_flight_controller.blueprint)
    app.register_blueprint(gateway_rating_controller.blueprint)
    app.register_blueprint(gateway_booking_controller.blueprint)
    app.register_blueprint(gateway_report_controller.blueprint)

    socketio.init_app(app)

    return app

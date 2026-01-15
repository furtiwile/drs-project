import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

db = SQLAlchemy()

from .domain import *

# Import repositories
from .repositories import (
    SqlAlchemyAirportRepository,
    SqlAlchemyAirlineRepository,
    SqlAlchemyFlightRepository,
    SqlAlchemyBookingRepository
)

# Import controllers
from .controllers import airport_bp

# Create a common blueprint for general routes
from flask import Blueprint
common_bp = Blueprint('common', __name__)

@common_bp.route('/')
def index():
    return {'message': 'Flight Service is running!', 'status': 'healthy'}

@common_bp.route('/health')
def health():
    return {'status': 'healthy', 'service': 'flight-service'}
# from .controllers.flight_controller import flight_bp
# from .controllers.airline_controller import airline_bp
# from .controllers.booking_controller import booking_bp

# Import websockets
from .websockets import socketio

# Import repository instances
from .repos import airport_repo, airline_repo, flight_repo, booking_repo

API_PREFIX = '/api/v1'

def create_app():
    app = Flask(__name__)

    # Configuration
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
    
    # Database configuration
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB2_URL', 'postgresql://user:password@localhost:5433/flights_db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Initialize extensions
    db.init_app(app)

    # Initialize SocketIO
    socketio.init_app(app, cors_allowed_origins="*")

    # Create services
    from .services.airport_service import AirportService
    airport_service = AirportService(airport_repo)

    # Create controllers
    from .controllers import AirportController
    airport_controller = AirportController(airport_service, airport_bp)

    # Register blueprints
    app.register_blueprint(common_bp, url_prefix=API_PREFIX)
    app.register_blueprint(airport_bp, url_prefix=API_PREFIX)
    # app.register_blueprint(flight_bp)  # TODO: implement
    # app.register_blueprint(airline_bp)  # TODO: implement
    # app.register_blueprint(booking_bp)  # TODO: implement
    
    return app

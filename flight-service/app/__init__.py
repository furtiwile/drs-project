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
from .controllers.flight_controller import flight_bp
from .controllers.airport_controller import airport_bp
from .controllers.airline_controller import airline_bp
from .controllers.booking_controller import booking_bp

# Import websockets
from .websockets import socketio

# Import repository instances
from .repos import airport_repo, airline_repo, flight_repo, booking_repo

def create_app():
    app = Flask(__name__)

    # Configuration
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
    
    # Database configuration
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB2_URL', 'postgresql://user:password@localhost:5433/flights_db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Initialize extensions
    db.init_app(app)
    CORS(app, resources={r"/api/*": {"origins": "*"}})

    # Initialize SocketIO
    socketio.init_app(app, cors_allowed_origins="*")

    # Register blueprints
    app.register_blueprint(flight_bp)
    app.register_blueprint(airport_bp)
    app.register_blueprint(airline_bp)
    app.register_blueprint(booking_bp)

    # Health check endpoint
    @app.route('/')
    def index():
        return {'message': 'Flight Service is running!', 'status': 'healthy'}

    @app.route('/api/v1/health')
    def health():
        return {'status': 'healthy', 'service': 'flight-service'}
    
    return app

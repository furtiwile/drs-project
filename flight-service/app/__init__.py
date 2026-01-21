import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

db = SQLAlchemy()

from .domain import *
from .controllers import (
    airport_bp,
    airline_bp,
    flight_bp,
    booking_bp,
    rating_bp
)

from flask import Blueprint
common_bp = Blueprint('common', __name__)

@common_bp.route('/')
def index():
    return {'message': 'Flight Service is running!', 'status': 'healthy'}

@common_bp.route('/health')
def health():
    return {'status': 'healthy', 'service': 'flight-service'}

API_PREFIX = '/api/v1'

def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
    
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB2_URL', 'postgresql://user:password@localhost:5433/flights_db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    CORS(app, resources={r"/api/*": {"origins": "*"}})

    # Create repositories
    from .repositories import (
    SqlAlchemyAirportRepository,
    SqlAlchemyAirlineRepository,
    SqlAlchemyFlightRepository,
    SqlAlchemyBookingRepository,
    SqlAlchemyRatingRepository
    )

    airport_repo = SqlAlchemyAirportRepository()
    airline_repo = SqlAlchemyAirlineRepository()
    flight_repo = SqlAlchemyFlightRepository()
    booking_repo = SqlAlchemyBookingRepository()
    rating_repo = SqlAlchemyRatingRepository()


    # Create services
    from .services import (
        AirportService,
        AirlineService,
        FlightService,
        BookingService,
        RatingService
    )
    
    airport_service = AirportService(airport_repo)
    airline_service = AirlineService(airline_repo)
    flight_service = FlightService(flight_repo, airport_repo, airline_repo)
    booking_service = BookingService(booking_repo, flight_repo)
    rating_service = RatingService(rating_repo, booking_repo)

    # Create controllers
    from .controllers import (
        AirportController,
        AirlineController,
        FlightController,
        BookingController,
        RatingController
    )
    
    airport_controller = AirportController(airport_service, airport_bp)
    airline_controller = AirlineController(airline_service, airline_bp)
    flight_controller = FlightController(flight_service, flight_bp)
    booking_controller = BookingController(booking_service, booking_bp)
    rating_controller = RatingController(rating_service, rating_bp)

    # Register routes for each blueprint(controller)
    app.register_blueprint(common_bp, url_prefix=API_PREFIX)
    app.register_blueprint(airport_bp, url_prefix=API_PREFIX)
    app.register_blueprint(airline_bp, url_prefix=API_PREFIX)
    app.register_blueprint(flight_bp, url_prefix=API_PREFIX)
    app.register_blueprint(booking_bp, url_prefix=API_PREFIX)
    app.register_blueprint(rating_bp, url_prefix=API_PREFIX)
    
    return app

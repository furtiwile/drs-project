import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

db = SQLAlchemy()

from .utils.logger_service import LoggerService, get_logger

logger = get_logger(__name__)

from .controllers import (
    airport_bp,
    airline_bp,
    flight_bp,
    booking_bp,
    rating_bp,
    report_bp,
    health_bp
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
    # Initialize logging system
    log_level = os.environ.get('LOG_LEVEL', 'INFO')
    log_file = os.environ.get('LOG_FILE', None)
    LoggerService.initialize(level=log_level, log_file=log_file)
    
    logger.info("Initializing Flight Service application")
    
    app = Flask(__name__)

    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
    
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB2_URL', 'postgresql://user:password@localhost:5433/flights_db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    CORS(app, resources={r"/api/*": {"origins": "*"}})
    logger.info("CORS configured for API endpoints")

    # Initialize WebSocket
    from .infrastructure.websocket.socket_manager import init_socketio
    socket_manager = init_socketio(app)

    # Initialize background task manager with app context
    from .infrastructure.tasks.task_manager import BackgroundTaskManager
    task_manager : BackgroundTaskManager = BackgroundTaskManager(app)
    task_manager.start()

    # Create repositories
    from .repositories import (
        SqlAlchemyAirportRepository,
        SqlAlchemyAirlineRepository,
        SqlAlchemyFlightRepository,
        SqlAlchemyBookingRepository,
        SqlAlchemyRatingRepository
    )
    from .repositories.report_repository import SqlAlchemyReportRepository

    airport_repo = SqlAlchemyAirportRepository()
    airline_repo = SqlAlchemyAirlineRepository()
    flight_repo = SqlAlchemyFlightRepository()
    booking_repo = SqlAlchemyBookingRepository()
    rating_repo = SqlAlchemyRatingRepository()
    report_repo = SqlAlchemyReportRepository()

    # Create services with dependencies
    from .services import (
        AirportService,
        AirlineService,
        FlightService,
        BookingService,
        RatingService
    )
    from .services.report_service import ReportService
    
    airport_service = AirportService(airport_repo)
    airline_service = AirlineService(airline_repo)
    booking_service = BookingService(
        booking_repo, 
        flight_repo,
        task_manager
    )
    flight_service = FlightService(
        flight_repo, 
        airport_repo, 
        airline_repo,
        booking_service,
        socket_manager
    )
    rating_service = RatingService(rating_repo, booking_repo)
    report_service = ReportService(report_repo)
    
    logger.info("All services instantiated successfully")

    # Create controllers
    from .controllers import (
        AirportController,
        AirlineController,
        FlightController,
        BookingController,
        RatingController,
        create_report_controller
    )
    
    airport_controller = AirportController(airport_service, airport_bp)
    airline_controller = AirlineController(airline_service, airline_bp)
    flight_controller = FlightController(flight_service, flight_bp)
    booking_controller = BookingController(booking_service, booking_bp)
    rating_controller = RatingController(rating_service, rating_bp)
    report_controller = create_report_controller(report_service)
    
    logger.info("All controllers instantiated successfully")

    # Register routes for each blueprint(controller)
    app.register_blueprint(common_bp, url_prefix=API_PREFIX)
    app.register_blueprint(airport_bp, url_prefix=API_PREFIX)
    app.register_blueprint(airline_bp, url_prefix=API_PREFIX)
    app.register_blueprint(flight_bp, url_prefix=API_PREFIX)
    app.register_blueprint(booking_bp, url_prefix=API_PREFIX)
    app.register_blueprint(rating_bp, url_prefix=API_PREFIX)
    app.register_blueprint(report_bp, url_prefix=API_PREFIX)
    app.register_blueprint(health_bp)
    
    logger.info("All blueprints registered successfully")
    
    # Initialize flight scheduler AFTER app is configured
    from .infrastructure.scheduler.flight_scheduler import init_flight_scheduler
    flight_scheduler = init_flight_scheduler(flight_repo, socket_manager, app)
    logger.info("Flight scheduler initialized")
    
    # Store socketio instance in app config for later use
    app.config['SOCKETIO'] = socket_manager.socketio
    
    logger.info("Flight Service application initialization complete")
    
    return app, socket_manager.socketio

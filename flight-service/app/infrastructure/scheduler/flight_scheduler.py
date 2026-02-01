"""
Flight Scheduler Service - Handles automatic flight status transitions
Following Clean Architecture principles
"""
import threading
import time
from datetime import datetime, timezone, timedelta
from typing import Optional
from ...domain.interfaces.repositories.iflight_repository import IFlightRepository
from ...domain.models.enums import FlightStatus
from ...domain.types.websocket_types import FlightNotificationData
from app.utils.logger_service import get_logger, LoggerService

logger = get_logger(__name__)

flight_scheduler: Optional[FlightScheduler] = None


class FlightScheduler:
    """
    Service that monitors flights and automatically transitions their status
    based on scheduled times
    """
    
    def __init__(self, flight_repository: IFlightRepository, socket_manager, app=None):
        self.flight_repository = flight_repository
        self.socket_manager = socket_manager
        self.app = app  # Store Flask app for context
        self.running = threading.Event()
        self.scheduler_thread: Optional[threading.Thread] = None
        self.check_interval = 10  # Check every 10 seconds
    
    def start(self):
        """Start the flight scheduler"""
        if not self.running.is_set():
            self.running.set()
            self.scheduler_thread = threading.Thread(target=self._run_scheduler, daemon=True)
            self.scheduler_thread.start()
            logger.info("Flight scheduler started")
    
    def stop(self):
        """Stop the flight scheduler"""
        self.running.clear()
        if self.scheduler_thread and self.scheduler_thread.is_alive():
            self.scheduler_thread.join(timeout=5)
        logger.info("Flight scheduler stopped")
    
    def _run_scheduler(self):
        """Main scheduler loop"""
        while self.running.is_set():
            try:
                self._check_and_update_flights()
                time.sleep(self.check_interval)
            except Exception as e:
                logger.error(f"Scheduler error: {str(e)}")
                time.sleep(self.check_interval)
    
    def _check_and_update_flights(self):
        """Check flights and update their status based on current time"""
        if not self.app:
            logger.warning("No Flask app context available, skipping flight checks")
            return
            
        try:
            # Push application context for database access
            with self.app.app_context():
                current_time = datetime.now(timezone.utc)
                
                # Start approved flights that have reached their departure time
                self._start_flights(current_time)
                
                # Complete flights that have reached their arrival time
                self._complete_flights(current_time)
            
        except Exception as e:
            LoggerService.log_error(logger, e, {'operation': 'check_flights'})
    
    def _start_flights(self, current_time: datetime):
        """Start flights that have reached their departure time"""
        try:
            # Get approved flights that should have started
            flights = self.flight_repository.get_flights_to_start(current_time)
            
            LoggerService.log_with_context(logger, 'DEBUG', 
                                         f'Checking flights to start at {current_time.isoformat()}',
                                         count=len(flights))
            
            for flight in flights:
                try:
                    flight.status = FlightStatus.IN_PROGRESS
                    flight.actual_start_time = current_time
                    self.flight_repository.update_flight(flight)
                    
                    LoggerService.log_business_event(logger, 'FLIGHT_AUTO_STARTED',
                                                   flight_id=flight.flight_id,
                                                   flight_name=flight.flight_name)
                    
                    # Notify via WebSocket
                    flight_data: FlightNotificationData = {
                        'flight_id': flight.flight_id,
                        'flight_name': flight.flight_name,
                        'status': 'IN_PROGRESS',
                        'departure_time': flight.departure_time.isoformat()
                    }
                    self.socket_manager.notify_flight_started(flight_data)
                except Exception as e:
                    LoggerService.log_error(logger, e, {'operation': 'start_flight', 'flight_id': flight.flight_id})
        except Exception as e:
            LoggerService.log_error(logger, e, {'operation': '_start_flights'})
    
    def _complete_flights(self, current_time: datetime):
        """Complete flights that have reached their arrival time"""
        try:
            # Get in-progress flights that should have completed
            flights = self.flight_repository.get_flights_to_complete(current_time)
            
            LoggerService.log_with_context(logger, 'DEBUG',
                                         f'Checking flights to complete at {current_time.isoformat()}',
                                         count=len(flights))
            
            for flight in flights:
                try:
                    flight.status = FlightStatus.COMPLETED
                    self.flight_repository.update_flight(flight)
                    
                    LoggerService.log_business_event(logger, 'FLIGHT_AUTO_COMPLETED',
                                                   flight_id=flight.flight_id,
                                                   flight_name=flight.flight_name)
                    
                    # Notify via WebSocket
                    flight_data: FlightNotificationData = {
                        'flight_id': flight.flight_id,
                        'flight_name': flight.flight_name,
                        'status': 'COMPLETED',
                        'departure_time': flight.departure_time.isoformat()
                    }
                    self.socket_manager.notify_flight_completed(flight_data)
                except Exception as e:
                    LoggerService.log_error(logger, e, {'operation': 'complete_flight', 'flight_id': flight.flight_id})
        except Exception as e:
            LoggerService.log_error(logger, e, {'operation': '_complete_flights'})


def init_flight_scheduler(flight_repository: IFlightRepository, socket_manager, app=None):
    """Initialize and start the flight scheduler"""
    global flight_scheduler
    flight_scheduler = FlightScheduler(flight_repository, socket_manager, app)
    flight_scheduler.start()
    return flight_scheduler

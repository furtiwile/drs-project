from typing import List
from datetime import datetime
from sqlalchemy import or_
from app.domain.models.flights import Flight
from app.domain.models.enums import FlightStatus
from app.domain.interfaces.repositories.ireport_repository import IReportRepository
from app import db
from app.utils.logger_service import get_logger, LoggerService

logger = get_logger(__name__)


class SqlAlchemyReportRepository(IReportRepository):
    """SQLAlchemy implementation of report repository"""

    def get_upcoming_flights(self) -> List[Flight]:
        """Get all upcoming flights (APPROVED status, not yet departed)"""
        LoggerService.log_with_context(logger, 'DEBUG', 'Getting upcoming flights')
        
        flights = Flight.query.options(
            db.joinedload(Flight.airline),
            db.joinedload(Flight.departure_airport),
            db.joinedload(Flight.arrival_airport)
        ).filter(
            Flight.status == FlightStatus.APPROVED,
            Flight.departure_time > datetime.utcnow()
        ).order_by(Flight.departure_time.asc()).all()
        
        LoggerService.log_with_context(logger, 'INFO', 'Retrieved upcoming flights',
                                      count=len(flights))
        return flights

    def get_in_progress_flights(self) -> List[Flight]:
        """Get all in-progress flights (IN_PROGRESS status)"""
        LoggerService.log_with_context(logger, 'DEBUG', 'Getting in-progress flights')
        
        flights = Flight.query.options(
            db.joinedload(Flight.airline),
            db.joinedload(Flight.departure_airport),
            db.joinedload(Flight.arrival_airport)
        ).filter(
            Flight.status == FlightStatus.IN_PROGRESS
        ).order_by(Flight.departure_time.asc()).all()
        
        LoggerService.log_with_context(logger, 'INFO', 'Retrieved in-progress flights',
                                      count=len(flights))
        return flights

    def get_completed_flights(self) -> List[Flight]:
        """Get all completed and cancelled flights"""
        LoggerService.log_with_context(logger, 'DEBUG', 'Getting completed/cancelled flights')
        
        flights = Flight.query.options(
            db.joinedload(Flight.airline),
            db.joinedload(Flight.departure_airport),
            db.joinedload(Flight.arrival_airport)
        ).filter(
            or_(
                Flight.status == FlightStatus.COMPLETED,
                Flight.status == FlightStatus.CANCELLED
            )
        ).order_by(Flight.updated_at.desc()).all()
        
        LoggerService.log_with_context(logger, 'INFO', 'Retrieved completed/cancelled flights',
                                      count=len(flights))
        return flights

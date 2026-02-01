"""
Logging Service Facade - Provides convenient access to logging functionality
This is a facade/adapter layer that wraps the infrastructure logging implementation
"""
from typing import Optional
from app.domain.interfaces.logging.ilogger import ILogger
from app.infrastructure.logging.log_manager import LogManager
from app.infrastructure.logging.log_strategies import (
    RequestLogStrategy,
    ResponseLogStrategy,
    BusinessEventLogStrategy,
    DatabaseOperationLogStrategy,
    ServiceCallLogStrategy
)


class LoggerService:
    """Facade for logging operations - delegates to infrastructure implementations"""
    
    @staticmethod
    def initialize(level: str = 'INFO', log_file: Optional[str] = None) -> None:
        """Initialize the logging system"""
        LogManager().initialize(level, log_file)
    
    @staticmethod
    def get_logger(name: str) -> ILogger:
        """Get a logger instance for a module"""
        return LogManager().get_logger(name)
    
    @staticmethod
    def log_request(logger: ILogger, method: str, endpoint: str, **context) -> None:
        """Log an incoming HTTP request"""
        RequestLogStrategy.log(logger, method, endpoint, **context)
    
    @staticmethod
    def log_response(logger: ILogger, method: str, endpoint: str, 
                    status_code: int, duration_ms: float, **context) -> None:
        """Log an HTTP response with timing information"""
        ResponseLogStrategy.log(logger, method, endpoint, status_code, duration_ms, **context)
    
    @staticmethod
    def log_business_event(logger: ILogger, event: str, **context) -> None:
        """Log an important business event"""
        BusinessEventLogStrategy.log(logger, event, **context)
    
    @staticmethod
    def log_database_operation(logger: ILogger, operation: str, table: str, **context) -> None:
        """Log a database operation"""
        DatabaseOperationLogStrategy.log(logger, operation, table, **context)
    
    @staticmethod
    def log_service_call(logger: ILogger, service: str, method: str, **context) -> None:
        """Log a service layer method call"""
        ServiceCallLogStrategy.log(logger, service, method, **context)
    
    @staticmethod
    def log_error(logger: ILogger, error: Exception, context: Optional[dict] = None) -> None:
        """Log an error with full context"""
        logger.error(
            f"Error occurred: {type(error).__name__}: {str(error)}",
            exception=error,
            **(context or {})
        )
    
    @staticmethod
    def log_with_context(logger: ILogger, level: str, message: str, **context) -> None:
        """Log a message with additional context"""
        log_method = getattr(logger, level.lower(), logger.info)
        log_method(message, **context)


def get_logger(name: str) -> ILogger:
    """Convenience function to get a logger instance"""
    return LoggerService.get_logger(name)


__all__ = ['LoggerService', 'get_logger']

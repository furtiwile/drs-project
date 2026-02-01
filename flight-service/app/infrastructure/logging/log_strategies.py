from app.domain.interfaces.logging.ilogger import ILogger


class RequestLogStrategy:
    """Strategy for logging HTTP requests"""
    
    @staticmethod
    def log(logger: ILogger, method: str, endpoint: str, **context) -> None:
        logger.info(
            f"Incoming request: {method} {endpoint}",
            method=method,
            endpoint=endpoint,
            **context
        )


class ResponseLogStrategy:
    """Strategy for logging HTTP responses"""
    
    @staticmethod
    def log(logger: ILogger, method: str, endpoint: str, status_code: int, 
            duration_ms: float, **context) -> None:
        level_method = 'info' if status_code < 400 else 'warning' if status_code < 500 else 'error'
        getattr(logger, level_method)(
            f"Response: {method} {endpoint} - {status_code} ({duration_ms:.2f}ms)",
            method=method,
            endpoint=endpoint,
            status_code=status_code,
            duration_ms=duration_ms,
            **context
        )


class BusinessEventLogStrategy:
    """Strategy for logging business events"""
    
    @staticmethod
    def log(logger: ILogger, event: str, **context) -> None:
        logger.info(
            f"Business event: {event}",
            event=event,
            **context
        )


class DatabaseOperationLogStrategy:
    """Strategy for logging database operations"""
    
    @staticmethod
    def log(logger: ILogger, operation: str, table: str, **context) -> None:
        logger.debug(
            f"Database operation: {operation} on {table}",
            operation=operation,
            table=table,
            **context
        )


class ServiceCallLogStrategy:
    """Strategy for logging service method calls"""
    
    @staticmethod
    def log(logger: ILogger, service: str, method: str, **context) -> None:
        logger.debug(
            f"Service call: {service}.{method}",
            service=service,
            method=method,
            **context
        )

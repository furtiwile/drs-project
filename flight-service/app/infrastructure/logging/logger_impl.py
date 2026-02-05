import logging
import traceback
from typing import Optional
from app.domain.interfaces.logging.ilogger import ILogger


class StructuredLogger(ILogger):
    """Concrete implementation of ILogger with structured logging support"""
    
    def __init__(self, name: str):
        self._logger = logging.getLogger(name)
    
    def debug(self, message: str, **context) -> None:
        self._log('DEBUG', message, **context)
    
    def info(self, message: str, **context) -> None:
        self._log('INFO', message, **context)
    
    def warning(self, message: str, **context) -> None:
        self._log('WARNING', message, **context)
    
    def error(self, message: str, exception: Optional[Exception] = None, **context) -> None:
        if exception:
            context.update({
                'error_type': type(exception).__name__,
                'error_message': str(exception),
                'traceback': traceback.format_exc()
            })
        self._log('ERROR', message, exc_info=exception, **context)
    
    def critical(self, message: str, **context) -> None:
        self._log('CRITICAL', message, **context)
    
    def _log(self, level: str, message: str, exc_info: Optional[Exception] = None, **context) -> None:
        log_method = getattr(self._logger, level.lower())
        extra = {'context': context} if context else {}
        if exc_info:
            log_method(message, exc_info=exc_info, extra=extra)
        else:
            log_method(message, extra=extra)

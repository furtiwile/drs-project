import logging
import sys
from typing import Optional, Dict
from app.domain.interfaces.logging.ilogger import ILogger
from app.infrastructure.logging.logger_impl import StructuredLogger
from app.infrastructure.logging.formatters import ColoredConsoleFormatter, PlainTextFormatter


class LogManager:
    """Manages logger initialization and configuration (Singleton)"""
    
    _instance: Optional['LogManager'] = None
    _initialized = False
    _loggers: Dict[str, ILogger] = {}
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def initialize(self, level: str = 'INFO', log_file: Optional[str] = None) -> None:
        """Initialize the logging system"""
        if self._initialized:
            return
        
        numeric_level = getattr(logging, level.upper(), logging.INFO)
        root_logger = logging.getLogger()
        root_logger.setLevel(numeric_level)
        
        for handler in root_logger.handlers[:]:
            root_logger.removeHandler(handler)
        
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(numeric_level)
        console_handler.setFormatter(ColoredConsoleFormatter())
        root_logger.addHandler(console_handler)
        
        if log_file:
            file_handler = logging.FileHandler(log_file)
            file_handler.setLevel(numeric_level)
            file_handler.setFormatter(PlainTextFormatter())
            root_logger.addHandler(file_handler)
        
        self._initialized = True
        root_logger.info("Logging system initialized")
    
    def get_logger(self, name: str) -> ILogger:
        """Get or create a logger instance"""
        if name not in self._loggers:
            self._loggers[name] = StructuredLogger(name)
        return self._loggers[name]

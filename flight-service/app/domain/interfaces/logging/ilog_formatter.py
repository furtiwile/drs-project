from abc import ABC, abstractmethod
import logging


class ILogFormatter(ABC):
    """Interface for log formatting"""
    
    @abstractmethod
    def format(self, record: logging.LogRecord) -> str:
        """Format a log record into a string"""

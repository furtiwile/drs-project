from abc import ABC, abstractmethod
from typing import 


class ILogger(ABC):
    """Interface for logging operations"""
    
    @abstractmethod
    def debug(self, message: str, **context) -> None:
        """Log debug message with optional context"""
    
    @abstractmethod
    def info(self, message: str, **context) -> None:
        """Log info message with optional context"""
    
    @abstractmethod
    def warning(self, message: str, **context) -> None:
        """Log warning message with optional context"""
    
    @abstractmethod
    def error(self, message: str, exception: Optional[Exception] = None, **context) -> None:
        """Log error message with optional exception and context"""
    
    @abstractmethod
    def critical(self, message: str, **context) -> None:
        """Log critical message with optional context"""

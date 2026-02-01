from abc import ABC, abstractmethod
from typing import Dict, Any, Optional


class ILogger(ABC):
    """Interface for logging operations"""
    
    @abstractmethod
    def debug(self, message: str, **context) -> None:
        """Log debug message with optional context"""
        pass
    
    @abstractmethod
    def info(self, message: str, **context) -> None:
        """Log info message with optional context"""
        pass
    
    @abstractmethod
    def warning(self, message: str, **context) -> None:
        """Log warning message with optional context"""
        pass
    
    @abstractmethod
    def error(self, message: str, exception: Optional[Exception] = None, **context) -> None:
        """Log error message with optional exception and context"""
        pass
    
    @abstractmethod
    def critical(self, message: str, **context) -> None:
        """Log critical message with optional context"""
        pass

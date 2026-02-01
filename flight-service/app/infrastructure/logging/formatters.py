import logging
import json
from datetime import datetime, timezone
from app.domain.interfaces.logging.ilog_formatter import ILogFormatter


class LogColors:
    """ANSI color codes for console output"""
    RESET = '\033[0m'
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GRAY = '\033[90m'
    BOLD = '\033[1m'


class ColoredConsoleFormatter(ILogFormatter, logging.Formatter):
    """Formatter that outputs colored, structured log messages"""
    
    LEVEL_COLORS = {
        'DEBUG': LogColors.GRAY,
        'INFO': LogColors.GREEN,
        'WARNING': LogColors.YELLOW,
        'ERROR': LogColors.RED,
        'CRITICAL': LogColors.RED + LogColors.BOLD
    }
    
    def format(self, record: logging.LogRecord) -> str:
        timestamp = datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z')
        level_color = self.LEVEL_COLORS.get(record.levelname, LogColors.RESET)
        
        parts = [
            f"{LogColors.GRAY}{timestamp}{LogColors.RESET}",
            f"{level_color}{record.levelname:8}{LogColors.RESET}",
            f"{LogColors.CYAN}[{record.name}]{LogColors.RESET}",
            f"{record.getMessage()}"
        ]
        
        if hasattr(record, 'context'):
            context = getattr(record, 'context', None)
            if context:
                context_str = json.dumps(context, default=str)
                parts.append(f"{LogColors.BLUE}| Context: {context_str}{LogColors.RESET}")
        
        if record.exc_info:
            exc_text = self.formatException(record.exc_info)
            parts.append(f"\n{LogColors.RED}{exc_text}{LogColors.RESET}")
        
        return " ".join(parts)


class PlainTextFormatter(ILogFormatter, logging.Formatter):
    """Plain text formatter for file output"""
    
    def __init__(self):
        super().__init__(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
    
    def format(self, record: logging.LogRecord) -> str:
        base_message = super().format(record)
        
        if hasattr(record, 'context'):
            context = getattr(record, 'context', None)
            if context:
                context_str = json.dumps(context, default=str)
                base_message += f" | Context: {context_str}"
        
        return base_message

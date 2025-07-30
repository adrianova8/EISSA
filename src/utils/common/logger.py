import sys
import logging
from typing import Optional
from datetime import datetime
from logging.handlers import RotatingFileHandler

from src.utils.common.names import BUSINESS_SHORT_NAME
from src.utils.common.paths import ProjectPaths

paths = ProjectPaths()

class CustomLogger:
    """
    A singleton logger class that provides logging functionality with file and console output.
    
    This class implements a singleton pattern to ensure only one logger instance exists.
    It supports multiple logging levels and rotating file handlers.
    
    Attributes:
        _instance (Optional[CustomLogger]): Singleton instance of the logger
        _logger (logging.Logger): Internal logger instance
    """
    
    _instance: Optional['CustomLogger'] = None
    
    def __new__(cls) -> 'CustomLogger':
        """
        Create or return the singleton instance of CustomLogger.
        
        Returns:
            CustomLogger: The singleton instance
        """
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialize_logger()
        return cls._instance

    def _initialize_logger(self) -> None:
        """
        Initialize the logger with custom configuration.
        
        Sets up file and console handlers with appropriate formatting and log levels.
        Creates necessary log directories if they don't exist.
        
        Raises:
            OSError: If log directory creation fails
            PermissionError: If there are permission issues
        """
        try:
            self._logger = logging.getLogger('CustomLogger')
            self._logger.setLevel(logging.DEBUG)
            
            # Create log directory if it doesn't exist
            log_dir = paths.logs_dir
            log_dir.mkdir(parents=True, exist_ok=True)
            
            # Custom formatter
            formatter = logging.Formatter(
                '%(asctime)s | %(levelname)-8s | %(message)s',
                datefmt='%Y-%m-%d %H:%M:%S'
            )
            
            datetime_str = datetime.now().strftime('%Y%m%d_%H%M%S')
            
            # Rotating file handler
            file_handler = RotatingFileHandler(
                filename=log_dir / f'app_{BUSINESS_SHORT_NAME}_{datetime_str}.log',
                maxBytes=10*1024*1024,
                backupCount=5,
                encoding='utf-8'
            )
            file_handler.setLevel(logging.DEBUG)
            file_handler.setFormatter(formatter)
            
            # Console handler
            console_handler = logging.StreamHandler(sys.stdout)
            console_handler.setLevel(logging.INFO)
            console_handler.setFormatter(formatter)
            
            # Clear existing handlers
            self._logger.handlers = []
            
            # Add handlers
            self._logger.addHandler(file_handler)
            self._logger.addHandler(console_handler)
            
        except OSError as e:
            self._logger.error(f"Error creating log directory: {e}")
            raise
        except Exception as e:
            self._logger.error(f"Unexpected error initializing logger: {e}")
            raise

    def debug(self, message: str) -> None:
        """
        Log a debug message.
        
        Args:
            message: The message to log
            
        Raises:
            ValueError: If message is empty or None
        """
        try:
            if not message:
                raise ValueError("Log message cannot be empty")
            self._logger.debug(message)
        except Exception as e:
            print(f"Error logging debug message: {e}")

    def info(self, message: str) -> None:
        """
        Log an info message.
        
        Args:
            message: The message to log
            
        Raises:
            ValueError: If message is empty or None
        """
        try:
            if not message:
                raise ValueError("Log message cannot be empty")
            self._logger.info(message)
        except Exception as e:
            print(f"Error logging info message: {e}")

    def warning(self, message: str) -> None:
        """
        Log a warning message.
        
        Args:
            message: The message to log
            
        Raises:
            ValueError: If message is empty or None
        """
        try:
            if not message:
                raise ValueError("Log message cannot be empty")
            self._logger.warning(message)
        except Exception as e:
            print(f"Error logging warning message: {e}")

    def error(self, message: str) -> None:
        """
        Log an error message.
        
        Args:
            message: The message to log
            
        Raises:
            ValueError: If message is empty or None
        """
        try:
            if not message:
                raise ValueError("Log message cannot be empty")
            self._logger.error(message)
        except Exception as e:
            print(f"Error logging error message: {e}")

    def critical(self, message: str) -> None:
        """
        Log a critical message.
        
        Args:
            message: The message to log
            
        Raises:
            ValueError: If message is empty or None
        """
        try:
            if not message:
                raise ValueError("Log message cannot be empty")
            self._logger.critical(message)
        except Exception as e:
            print(f"Error logging critical message: {e}")

if __name__ == "__main__":
    # Create an instance of the logger
    logger = CustomLogger()
"""
Nia LeSane - Comprehensive Logging Configuration
Production-grade error logging across Python, PowerShell, and GitHub Actions workflows.
"""

import logging
import logging.handlers
import os
from datetime import datetime
from pathlib import Path

# Create logs directory if it doesn't exist
LOG_DIR = Path(__file__).parent.parent / "logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)

# Log file paths
ERROR_LOG = LOG_DIR / "nia_errors.log"
INFO_LOG = LOG_DIR / "nia_info.log"
AUDIT_LOG = LOG_DIR / "nia_audit.log"

# Timestamp format for logs
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s"
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"


def setup_logging(logger_name="nia_core"):
    """
    Configure comprehensive logging for Nia LeSane core components.
    
    Logs to:
    - File: ERROR level and above (errors, critical failures)
    - File: INFO level and above (general application flow)
    - File: AUDIT level for compliance/tracking
    - Console: WARNING level and above
    
    Args:
        logger_name (str): Name of the logger instance
        
    Returns:
        logging.Logger: Configured logger instance
    """
    logger = logging.getLogger(logger_name)
    
    # Only configure if not already configured
    if logger.handlers:
        return logger
    
    logger.setLevel(logging.DEBUG)
    
    # === FILE HANDLER: Errors ===
    error_handler = logging.FileHandler(ERROR_LOG, encoding='utf-8')
    error_handler.setLevel(logging.ERROR)
    error_formatter = logging.Formatter(LOG_FORMAT, datefmt=DATE_FORMAT)
    error_handler.setFormatter(error_formatter)
    logger.addHandler(error_handler)
    
    # === FILE HANDLER: Info (with rotation) ===
    info_handler = logging.handlers.RotatingFileHandler(
        INFO_LOG,
        maxBytes=10*1024*1024,  # 10 MB
        backupCount=5,  # Keep 5 backups
        encoding='utf-8'
    )
    info_handler.setLevel(logging.INFO)
    info_formatter = logging.Formatter(LOG_FORMAT, datefmt=DATE_FORMAT)
    info_handler.setFormatter(info_formatter)
    logger.addHandler(info_handler)
    
    # === FILE HANDLER: Audit ===
    audit_handler = logging.FileHandler(AUDIT_LOG, encoding='utf-8')
    audit_handler.setLevel(logging.INFO)
    audit_formatter = logging.Formatter(
        "%(asctime)s - AUDIT - %(levelname)s - %(message)s",
        datefmt=DATE_FORMAT
    )
    audit_handler.setFormatter(audit_formatter)
    logger.addHandler(audit_handler)
    
    # === CONSOLE HANDLER: Warnings and above ===
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.WARNING)
    console_formatter = logging.Formatter(
        "%(levelname)s: %(message)s [%(name)s]"
    )
    console_handler.setFormatter(console_formatter)
    logger.addHandler(console_handler)
    
    return logger


# Create default logger instance
logger = setup_logging("nia_core")


class LogContext:
    """Context manager for logging operation blocks with timing."""
    
    def __init__(self, operation_name, logger_instance=None):
        self.operation = operation_name
        self.logger = logger_instance or logger
        self.start_time = None
        
    def __enter__(self):
        self.start_time = datetime.now()
        self.logger.info(f"START: {self.operation}")
        return self
        
    def __exit__(self, exc_type, exc_val, exc_tb):
        duration = (datetime.now() - self.start_time).total_seconds()
        
        if exc_type is None:
            self.logger.info(f"COMPLETE: {self.operation} ({duration:.2f}s)")
        else:
            self.logger.error(
                f"FAILED: {self.operation} after {duration:.2f}s - {exc_type.__name__}: {exc_val}",
                exc_info=True
            )
        return False  # Don't suppress exceptions

"""
Logging configuration for Trello MCP Server

This module sets up structured JSON logging optimized for Google Cloud Run.
"""

import logging
import sys
import json
from datetime import datetime
from typing import Any, Dict

from config import config


class CloudRunFormatter(logging.Formatter):
    """Custom formatter for Cloud Run structured logging"""
    
    def format(self, record: logging.LogRecord) -> str:
        # Create structured log entry
        log_entry = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "severity": record.levelname,
            "message": record.getMessage(),
            "logger": record.name,
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno
        }
        
        # Add exception info if present
        if record.exc_info:
            log_entry["exception"] = self.formatException(record.exc_info)
            
        # Add extra fields
        if hasattr(record, 'extra_fields'):
            log_entry.update(record.extra_fields)
            
        # Add Cloud Run specific fields
        if config.is_cloud_run():
            log_entry["service"] = config.SERVICE_NAME
            log_entry["version"] = config.SERVICE_VERSION
            
        return json.dumps(log_entry, ensure_ascii=False)


def setup_logging() -> logging.Logger:
    """Setup logging configuration"""
    
    # Get root logger
    root_logger = logging.getLogger()
    
    # Clear existing handlers
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)
        
    # Create console handler
    console_handler = logging.StreamHandler(sys.stdout)
    
    # Set formatter based on environment
    if config.is_cloud_run() or config.LOG_FORMAT == "json":
        formatter = CloudRunFormatter()
    else:
        # Use simple format for local development
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        
    console_handler.setFormatter(formatter)
    root_logger.addHandler(console_handler)
    
    # Set log level
    log_level = getattr(logging, config.LOG_LEVEL.upper(), logging.INFO)
    root_logger.setLevel(log_level)
    
    # Reduce noise from third-party libraries
    logging.getLogger("aiohttp").setLevel(logging.WARNING)
    logging.getLogger("urllib3").setLevel(logging.WARNING)
    logging.getLogger("asyncio").setLevel(logging.WARNING)
    
    # Create application logger
    logger = logging.getLogger("trello_mcp")
    logger.info("Logging configured successfully")
    
    return logger
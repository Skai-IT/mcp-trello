"""
Configuration module for Trello MCP Server

This module provides configuration settings optimized for Google Cloud Run deployment.
"""

import os
from datetime import datetime, timezone


class Config:
    """Configuration settings for the Trello MCP server"""
    
    # Server settings
    DEBUG = os.getenv("DEBUG", "false").lower() == "true"
    PORT = int(os.getenv("PORT", 8080))
    
    # Cloud Run specific settings
    SERVICE_NAME = os.getenv("K_SERVICE", "trello-mcp")
    SERVICE_VERSION = os.getenv("K_REVISION", "unknown")
    
    # Logging settings
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    LOG_FORMAT = "json"  # Use JSON format for Cloud Logging
    
    # API settings
    REQUEST_TIMEOUT = int(os.getenv("REQUEST_TIMEOUT", 30))
    MAX_RETRIES = int(os.getenv("MAX_RETRIES", 3))
    
    @staticmethod
    def get_timestamp() -> str:
        """Get current timestamp in ISO format"""
        return datetime.now(timezone.utc).isoformat()
        
    @staticmethod
    def is_cloud_run() -> bool:
        """Check if running in Cloud Run environment"""
        return os.getenv("K_SERVICE") is not None


# Global config instance
config = Config()
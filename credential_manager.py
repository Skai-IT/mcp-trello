"""
Credential Manager for Trello MCP

Handles session-based credential storage and browser-based OAuth login.
Supports both interactive prompt-based and session-cached credentials.
Can also use environment variables for pre-configured authentication.
"""

import logging
from typing import Optional, Tuple
from datetime import datetime, timedelta
import webbrowser
import json
from config import config

logger = logging.getLogger(__name__)


class CredentialManager:
    """Manages Trello API credentials with session caching"""
    
    def __init__(self, cache_duration_minutes: int = 480):
        """
        Initialize credential manager
        
        Args:
            cache_duration_minutes: How long credentials are valid in session (default: 8 hours)
        """
        self.cache_duration = timedelta(minutes=cache_duration_minutes)
        self.cached_credentials: Optional[dict] = None
        self.credentials_timestamp: Optional[datetime] = None
        self.session_id: Optional[str] = None
        
        # Load from environment variables if available
        self.env_username = config.TRELLO_USERNAME
        self.env_password = config.TRELLO_PASSWORD
        
        # Cache environment credentials if both provided
        if self.env_username and self.env_password:
            logger.info("Loading credentials from environment variables (TRELLO_USERNAME, TRELLO_PASSWORD)")
            self.cache_credentials(self.env_username, self.env_password)
        
    def is_cached_valid(self) -> bool:
        """Check if cached credentials are still valid"""
        if not self.cached_credentials or not self.credentials_timestamp:
            return False
        
        if datetime.now() - self.credentials_timestamp > self.cache_duration:
            logger.info("Cached credentials expired")
            self.cached_credentials = None
            self.credentials_timestamp = None
            return False
        
        return True
    
    def cache_credentials(self, api_key: str, token: str, username: str = None, password: str = None) -> None:
        """
        Cache credentials for the session
        
        Args:
            api_key: Trello API key
            token: Trello API token
            username: Optional username (e.g., from environment variable)
            password: Optional password (e.g., from environment variable)
        """
        self.cached_credentials = {
            "api_key": api_key,
            "token": token,
            "username": username,
            "password": password
        }
        self.credentials_timestamp = datetime.now()
        logger.info("Credentials cached for session")
    
    def get_cached_credentials(self) -> Optional[Tuple[str, str]]:
        """
        Get cached credentials if still valid
        
        Returns:
            Tuple of (api_key, token) or None if not cached/expired
        """
        if self.is_cached_valid() and self.cached_credentials:
            return (
                self.cached_credentials["api_key"],
                self.cached_credentials["token"]
            )
        return None
    
    def get_or_prompt_credentials(
        self, 
        api_key: Optional[str] = None, 
        token: Optional[str] = None
    ) -> Tuple[str, str]:
        """
        Get credentials from cache, parameters, or prompt user
        
        Priority:
        1. Use provided credentials
        2. Use cached credentials if valid
        3. Prompt user to login
        
        Args:
            api_key: Optional API key to use
            token: Optional token to use
            
        Returns:
            Tuple of (api_key, token)
            
        Raises:
            ValueError: If credentials cannot be obtained
        """
        # Priority 1: Use provided credentials
        if api_key and token:
            logger.info("Using provided credentials")
            self.cache_credentials(api_key, token)
            return (api_key, token)
        
        # Priority 2: Use cached credentials if valid
        cached = self.get_cached_credentials()
        if cached:
            logger.info("Using cached credentials from session")
            return cached
        
        # Priority 3: Prompt user to login
        logger.info("No credentials provided or cached, prompting user to login")
        return self.prompt_for_credentials()
    
    def prompt_for_credentials(self) -> Tuple[str, str]:
        """
        Prompt user to get Trello credentials from https://trello.com/app-key
        
        Returns:
            Tuple of (api_key, token)
            
        Raises:
            ValueError: If user doesn't provide credentials
        """
        print("\n" + "="*60)
        print("🔐 TRELLO LOGIN REQUIRED")
        print("="*60)
        print("\nPlease authenticate with Trello:")
        print("\n1. A browser window will open to https://trello.com/app-key")
        print("2. Copy your API Key (shown at the top)")
        print("3. Click 'Token' link to generate/view your Token")
        print("4. Return here and paste both values")
        print("\n" + "-"*60 + "\n")
        
        # Open browser to Trello app-key page
        try:
            webbrowser.open("https://trello.com/app-key")
            logger.info("Opened Trello API key page in browser")
        except Exception as e:
            logger.warning(f"Could not open browser: {e}")
            print("Could not automatically open browser.")
            print("Please manually visit: https://trello.com/app-key")
        
        print()
        
        # Get API key from user
        while True:
            api_key = input("📋 Enter your Trello API Key: ").strip()
            if api_key and len(api_key) >= 32:
                break
            print("❌ Invalid API key. Should be at least 32 characters.\n")
        
        # Get token from user
        while True:
            token = input("🔑 Enter your Trello Token: ").strip()
            if token and len(token) >= 32:
                break
            print("❌ Invalid token. Should be at least 32 characters.\n")
        
        print("\n✅ Credentials received and cached for this session\n")
        print("="*60 + "\n")
        
        # Cache the credentials
        self.cache_credentials(api_key, token)
        
        return (api_key, token)
    
    def get_login_url(self) -> str:
        """
        Get the Trello login URL
        
        Returns:
            URL for user to get API credentials
        """
        return "https://trello.com/app-key"
    
    def clear_credentials(self) -> None:
        """Clear all cached credentials"""
        self.cached_credentials = None
        self.credentials_timestamp = None
        logger.info("Credentials cleared")
    
    def get_session_info(self) -> dict:
        """
        Get information about current session
        
        Returns:
            Dictionary with session info
        """
        return {
            "has_cached_credentials": self.is_cached_valid(),
            "cache_duration_minutes": int(self.cache_duration.total_seconds() / 60),
            "credentials_timestamp": self.credentials_timestamp.isoformat() if self.credentials_timestamp else None,
            "login_url": self.get_login_url()
        }

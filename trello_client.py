"""
Trello API Client

This module provides a comprehensive wrapper around the Trello REST API.
Handles authentication, rate limiting, and all API operations.
"""

import asyncio
import logging
import time
from typing import Any, Dict, List, Optional
from datetime import datetime, timedelta

import aiohttp
from pydantic import ValidationError

from schemas import (
    TrelloCredentials, BoardResponse, ListResponse, CardResponse,
    CreateBoardRequest, CreateListRequest, CreateCardRequest,
    UpdateBoardRequest, UpdateCardRequest, SearchRequest
)

logger = logging.getLogger(__name__)


class RateLimiter:
    """Rate limiter for Trello API (300 requests per 10 seconds)"""
    
    def __init__(self, max_requests: int = 300, time_window: int = 10):
        self.max_requests = max_requests
        self.time_window = time_window
        self.requests = []
        self._lock = asyncio.Lock()
        
    async def acquire(self):
        """Acquire permission to make a request"""
        async with self._lock:
            now = time.time()
            
            # Remove old requests outside the time window
            self.requests = [req_time for req_time in self.requests 
                           if now - req_time < self.time_window]
            
            # Check if we can make a new request
            if len(self.requests) >= self.max_requests:
                # Calculate wait time
                oldest_request = min(self.requests)
                wait_time = self.time_window - (now - oldest_request)
                if wait_time > 0:
                    logger.warning(f"Rate limit reached, waiting {wait_time:.2f} seconds")
                    await asyncio.sleep(wait_time)
                    return await self.acquire()
                    
            # Record this request
            self.requests.append(now)
            

class TrelloAPIError(Exception):
    """Custom exception for Trello API errors"""
    
    def __init__(self, message: str, status_code: int = None, response_data: Any = None):
        super().__init__(message)
        self.status_code = status_code
        self.response_data = response_data


class TrelloClient:
    """Trello API client with full functionality"""
    
    def __init__(self):
        self.base_url = "https://api.trello.com/1"
        self.rate_limiter = RateLimiter()
        self._session = None
        
    async def _get_session(self) -> aiohttp.ClientSession:
        """Get or create HTTP session"""
        if self._session is None or self._session.closed:
            timeout = aiohttp.ClientTimeout(total=30)
            self._session = aiohttp.ClientSession(
                timeout=timeout,
                headers={
                    'User-Agent': 'Trello-MCP-Server/1.0.0',
                    'Accept': 'application/json',
                    'Content-Type': 'application/json'
                }
            )
        return self._session
        
    async def close(self):
        """Close HTTP session"""
        if self._session and not self._session.closed:
            await self._session.close()
            
    async def _make_request(
        self,
        method: str,
        endpoint: str,
        credentials: TrelloCredentials,
        params: Optional[Dict[str, Any]] = None,
        json_data: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Make authenticated request to Trello API"""
        
        # Rate limiting
        await self.rate_limiter.acquire()
        
        # Prepare parameters with authentication
        if params is None:
            params = {}
            
        params.update({
            'key': credentials.api_key,
            'token': credentials.token
        })
        
        # Make request
        session = await self._get_session()
        url = f"{self.base_url}/{endpoint}"
        
        try:
            logger.info(f"Making {method} request to {endpoint}")
            
            async with session.request(
                method=method,
                url=url,
                params=params,
                json=json_data
            ) as response:
                
                response_text = await response.text()
                
                # Handle different response types
                if response.status == 200:
                    try:
                        return await response.json()
                    except Exception:
                        # Some endpoints return plain text
                        return {"result": response_text}
                        
                elif response.status == 401:
                    raise TrelloAPIError(
                        "Unauthorized - check your API key and token",
                        response.status,
                        response_text
                    )
                elif response.status == 403:
                    raise TrelloAPIError(
                        "Forbidden - insufficient permissions",
                        response.status,
                        response_text
                    )
                elif response.status == 404:
                    raise TrelloAPIError(
                        "Not found - the requested resource does not exist",
                        response.status,
                        response_text
                    )
                elif response.status == 429:
                    raise TrelloAPIError(
                        "Rate limit exceeded",
                        response.status,
                        response_text
                    )
                else:
                    raise TrelloAPIError(
                        f"API request failed with status {response.status}",
                        response.status,
                        response_text
                    )
                    
        except aiohttp.ClientError as e:
            raise TrelloAPIError(f"Network error: {str(e)}")
            
    async def validate_credentials(self, credentials: TrelloCredentials) -> Dict[str, Any]:
        """Validate Trello credentials"""
        try:
            # Try to get member information
            response = await self._make_request(
                "GET", "members/me", credentials,
                params={"fields": "id,username,fullName,email"}
            )
            
            return {
                "valid": True,
                "user_info": response
            }
            
        except TrelloAPIError as e:
            logger.error(f"Credential validation failed: {e}")
            return {
                "valid": False,
                "error": str(e)
            }
            
    # Board Management
    async def list_boards(self, credentials: TrelloCredentials) -> List[Dict[str, Any]]:
        """List all boards for the authenticated user"""
        try:
            response = await self._make_request(
                "GET", "members/me/boards", credentials,
                params={
                    "fields": "id,name,desc,closed,url,prefs",
                    "filter": "open"
                }
            )
            
            return response if isinstance(response, list) else []
            
        except TrelloAPIError:
            raise
            
    async def get_board(self, credentials: TrelloCredentials, board_id: str) -> Dict[str, Any]:
        """Get detailed information about a specific board"""
        try:
            response = await self._make_request(
                "GET", f"boards/{board_id}", credentials,
                params={
                    "fields": "id,name,desc,closed,url,prefs,labelNames",
                    "lists": "open",
                    "cards": "open",
                    "members": "all"
                }
            )
            
            return response
            
        except TrelloAPIError:
            raise
            
    async def create_board(
        self,
        credentials: TrelloCredentials,
        request: CreateBoardRequest
    ) -> Dict[str, Any]:
        """Create a new board"""
        try:
            params = {
                "name": request.name,
                "defaultLists": request.default_lists
            }
            
            if request.desc:
                params["desc"] = request.desc
            if request.organization_id:
                params["idOrganization"] = request.organization_id
            if request.prefs:
                for key, value in request.prefs.items():
                    params[f"prefs_{key}"] = value
                    
            response = await self._make_request(
                "POST", "boards", credentials, params=params
            )
            
            return response
            
        except TrelloAPIError:
            raise
            
    async def update_board(
        self,
        credentials: TrelloCredentials,
        board_id: str,
        request: UpdateBoardRequest
    ) -> Dict[str, Any]:
        """Update an existing board"""
        try:
            params = {}
            
            if request.name is not None:
                params["name"] = request.name
            if request.desc is not None:
                params["desc"] = request.desc
            if request.closed is not None:
                params["closed"] = request.closed
            if request.prefs:
                for key, value in request.prefs.items():
                    params[f"prefs_{key}"] = value
                    
            response = await self._make_request(
                "PUT", f"boards/{board_id}", credentials, params=params
            )
            
            return response
            
        except TrelloAPIError:
            raise
            
    # List Management
    async def get_lists(self, credentials: TrelloCredentials, board_id: str) -> List[Dict[str, Any]]:
        """Get all lists on a board"""
        try:
            response = await self._make_request(
                "GET", f"boards/{board_id}/lists", credentials,
                params={
                    "fields": "id,name,closed,pos",
                    "filter": "open"
                }
            )
            
            return response if isinstance(response, list) else []
            
        except TrelloAPIError:
            raise
            
    async def create_list(
        self,
        credentials: TrelloCredentials,
        request: CreateListRequest
    ) -> Dict[str, Any]:
        """Create a new list on a board"""
        try:
            params = {
                "name": request.name,
                "idBoard": request.board_id
            }
            
            if request.pos is not None:
                params["pos"] = request.pos
                
            response = await self._make_request(
                "POST", "lists", credentials, params=params
            )
            
            return response
            
        except TrelloAPIError:
            raise
            
    # Card Management
    async def get_cards(
        self,
        credentials: TrelloCredentials,
        board_id: Optional[str] = None,
        list_id: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """Get cards from a board or list"""
        try:
            if list_id:
                endpoint = f"lists/{list_id}/cards"
            elif board_id:
                endpoint = f"boards/{board_id}/cards"
            else:
                raise TrelloAPIError("Either board_id or list_id must be provided")
                
            response = await self._make_request(
                "GET", endpoint, credentials,
                params={
                    "fields": "id,name,desc,closed,due,url,labels,members",
                    "filter": "open"
                }
            )
            
            return response if isinstance(response, list) else []
            
        except TrelloAPIError:
            raise
            
    async def create_card(
        self,
        credentials: TrelloCredentials,
        request: CreateCardRequest
    ) -> Dict[str, Any]:
        """Create a new card"""
        try:
            params = {
                "name": request.name,
                "idList": request.list_id
            }
            
            if request.desc:
                params["desc"] = request.desc
            if request.pos is not None:
                params["pos"] = request.pos
            if request.due:
                params["due"] = request.due.isoformat()
            if request.labels:
                params["idLabels"] = ",".join(request.labels)
            if request.members:
                params["idMembers"] = ",".join(request.members)
                
            response = await self._make_request(
                "POST", "cards", credentials, params=params
            )
            
            return response
            
        except TrelloAPIError:
            raise
            
    async def update_card(
        self,
        credentials: TrelloCredentials,
        card_id: str,
        request: UpdateCardRequest
    ) -> Dict[str, Any]:
        """Update an existing card"""
        try:
            params = {}
            
            if request.name is not None:
                params["name"] = request.name
            if request.desc is not None:
                params["desc"] = request.desc
            if request.closed is not None:
                params["closed"] = request.closed
            if request.list_id is not None:
                params["idList"] = request.list_id
            if request.pos is not None:
                params["pos"] = request.pos
            if request.due is not None:
                params["due"] = request.due.isoformat() if request.due else None
                
            response = await self._make_request(
                "PUT", f"cards/{card_id}", credentials, params=params
            )
            
            return response
            
        except TrelloAPIError:
            raise
            
    async def add_member_to_card(
        self,
        credentials: TrelloCredentials,
        card_id: str,
        member_id: str
    ) -> Dict[str, Any]:
        """Add a member to a card"""
        try:
            response = await self._make_request(
                "POST", f"cards/{card_id}/idMembers", credentials,
                params={"value": member_id}
            )
            
            return response
            
        except TrelloAPIError:
            raise
            
    async def search_cards(
        self,
        credentials: TrelloCredentials,
        request: SearchRequest
    ) -> List[Dict[str, Any]]:
        """Search for cards"""
        try:
            params = {
                "query": request.query,
                "modelTypes": "cards",
                "cards_limit": request.limit or 50
            }
            
            if request.board_ids:
                params["idBoards"] = ",".join(request.board_ids)
                
            response = await self._make_request(
                "GET", "search", credentials, params=params
            )
            
            # Extract cards from search response
            cards = response.get("cards", []) if isinstance(response, dict) else []
            return cards
            
        except TrelloAPIError:
            raise
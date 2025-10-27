"""
Pydantic schemas for Trello MCP Server

This module defines all data models and validation schemas using Pydantic.
Provides type safety and validation for API requests and responses.
"""

from datetime import datetime
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field, validator


class TrelloCredentials(BaseModel):
    """Trello API credentials"""
    api_key: str = Field(..., description="Trello API key")
    token: str = Field(..., description="Trello API token")
    
    @validator('api_key', 'token')
    def validate_not_empty(cls, v):
        if not v or not v.strip():
            raise ValueError("API key and token cannot be empty")
        return v.strip()


class BoardPreferences(BaseModel):
    """Board preference settings"""
    permissionLevel: Optional[str] = Field(None, description="Permission level")
    voting: Optional[str] = Field(None, description="Voting permissions") 
    comments: Optional[str] = Field(None, description="Comment permissions")
    background: Optional[str] = Field(None, description="Board background")


class CreateBoardRequest(BaseModel):
    """Request model for creating a board"""
    name: str = Field(..., description="Board name")
    desc: Optional[str] = Field(None, description="Board description")
    organization_id: Optional[str] = Field(None, description="Organization ID")
    default_lists: bool = Field(True, description="Create default lists")
    prefs: Optional[Dict[str, Any]] = Field(None, description="Board preferences")
    
    @validator('name')
    def validate_name(cls, v):
        if not v or not v.strip():
            raise ValueError("Board name cannot be empty")
        if len(v.strip()) > 16384:
            raise ValueError("Board name cannot exceed 16384 characters")
        return v.strip()


class UpdateBoardRequest(BaseModel):
    """Request model for updating a board"""
    name: Optional[str] = Field(None, description="New board name")
    desc: Optional[str] = Field(None, description="New board description")
    closed: Optional[bool] = Field(None, description="Whether board is closed")
    prefs: Optional[Dict[str, Any]] = Field(None, description="Board preferences")
    
    @validator('name', pre=True, always=True)
    def validate_name(cls, v):
        if v is not None:
            if not v.strip():
                raise ValueError("Board name cannot be empty")
            if len(v.strip()) > 16384:
                raise ValueError("Board name cannot exceed 16384 characters")
            return v.strip()
        return v


class CreateListRequest(BaseModel):
    """Request model for creating a list"""
    name: str = Field(..., description="List name")
    board_id: str = Field(..., description="Board ID")
    pos: Optional[str] = Field(None, description="List position")
    
    @validator('name')
    def validate_name(cls, v):
        if not v or not v.strip():
            raise ValueError("List name cannot be empty")
        if len(v.strip()) > 16384:
            raise ValueError("List name cannot exceed 16384 characters")
        return v.strip()
        
    @validator('board_id')
    def validate_board_id(cls, v):
        if not v or not v.strip():
            raise ValueError("Board ID cannot be empty")
        return v.strip()


class CreateCardRequest(BaseModel):
    """Request model for creating a card"""
    name: str = Field(..., description="Card name")
    list_id: str = Field(..., description="List ID")
    desc: Optional[str] = Field(None, description="Card description")
    pos: Optional[str] = Field(None, description="Card position")
    due: Optional[datetime] = Field(None, description="Due date")
    labels: Optional[List[str]] = Field(None, description="Label IDs")
    members: Optional[List[str]] = Field(None, description="Member IDs")
    
    @validator('name')
    def validate_name(cls, v):
        if not v or not v.strip():
            raise ValueError("Card name cannot be empty")
        if len(v.strip()) > 16384:
            raise ValueError("Card name cannot exceed 16384 characters")
        return v.strip()
        
    @validator('list_id')
    def validate_list_id(cls, v):
        if not v or not v.strip():
            raise ValueError("List ID cannot be empty")
        return v.strip()


class UpdateCardRequest(BaseModel):
    """Request model for updating a card"""
    name: Optional[str] = Field(None, description="New card name")
    desc: Optional[str] = Field(None, description="New card description")
    closed: Optional[bool] = Field(None, description="Whether card is closed")
    list_id: Optional[str] = Field(None, description="Move to this list")
    pos: Optional[str] = Field(None, description="New position")
    due: Optional[datetime] = Field(None, description="Due date (null to remove)")
    
    @validator('name', pre=True, always=True)
    def validate_name(cls, v):
        if v is not None:
            if not v.strip():
                raise ValueError("Card name cannot be empty")
            if len(v.strip()) > 16384:
                raise ValueError("Card name cannot exceed 16384 characters")
            return v.strip()
        return v


class SearchRequest(BaseModel):
    """Request model for searching cards"""
    query: str = Field(..., description="Search query")
    board_ids: Optional[List[str]] = Field(None, description="Board IDs to search in")
    limit: Optional[int] = Field(50, description="Maximum results")
    
    @validator('query')
    def validate_query(cls, v):
        if not v or not v.strip():
            raise ValueError("Search query cannot be empty")
        return v.strip()
        
    @validator('limit')
    def validate_limit(cls, v):
        if v is not None and (v < 1 or v > 1000):
            raise ValueError("Limit must be between 1 and 1000")
        return v


# Response models
class BoardResponse(BaseModel):
    """Response model for board data"""
    id: str
    name: str
    desc: Optional[str] = None
    closed: bool = False
    url: Optional[str] = None
    prefs: Optional[Dict[str, Any]] = None


class ListResponse(BaseModel):
    """Response model for list data"""
    id: str
    name: str
    closed: bool = False
    pos: Optional[float] = None
    board_id: Optional[str] = Field(None, alias="idBoard")


class CardResponse(BaseModel):
    """Response model for card data"""
    id: str
    name: str
    desc: Optional[str] = None
    closed: bool = False
    url: Optional[str] = None
    due: Optional[datetime] = None
    list_id: Optional[str] = Field(None, alias="idList")
    labels: Optional[List[Dict[str, Any]]] = None
    members: Optional[List[Dict[str, Any]]] = None
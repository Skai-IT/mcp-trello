"""
Trello MCP Tools

This module implements all 11 MCP tools for Trello integration:
- Board management: list_boards, get_board, create_board, update_board
- List management: get_lists, create_list
- Card management: get_cards, create_card, update_card, add_member_to_card, search_cards
"""

import logging
from typing import Any, Dict, List, Optional

from trello_client import TrelloClient, TrelloAPIError
from credential_manager import CredentialManager
from schemas import (
    TrelloCredentials, CreateBoardRequest, CreateListRequest, 
    CreateCardRequest, UpdateBoardRequest, UpdateCardRequest, SearchRequest
)

logger = logging.getLogger(__name__)


class TrelloTools:
    """Implementation of all Trello MCP tools"""
    
    def __init__(self):
        self.client = None  # Lazy initialize
        self.credential_manager = CredentialManager()
    
    def get_client(self) -> TrelloClient:
        """Get or initialize TrelloClient"""
        if self.client is None:
            self.client = TrelloClient()
        return self.client
        
    def get_tools(self) -> Dict[str, Dict[str, Any]]:
        """Get all available tools with their schemas"""
        return {
            "list_boards": {
                "description": "List all boards for the authenticated user (credentials optional - will prompt if needed)",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "api_key": {
                            "type": "string",
                            "description": "Trello API key (optional, will prompt if not provided)"
                        },
                        "token": {
                            "type": "string", 
                            "description": "Trello API token (optional, will prompt if not provided)"
                        }
                    },
                    "required": []
                }
            },
            "get_board": {
                "description": "Get detailed information about a specific board",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "api_key": {"type": "string", "description": "Trello API key (optional, will prompt if not provided)"},
                        "token": {"type": "string", "description": "Trello API token (optional, will prompt if not provided)"},
                        "board_id": {"type": "string", "description": "ID of the board to retrieve"}
                    },
                    "required": ["board_id"]
                }
            },
            "create_board": {
                "description": "Create a new board",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "api_key": {"type": "string", "description": "Trello API key (optional, will prompt if not provided)"},
                        "token": {"type": "string", "description": "Trello API token (optional, will prompt if not provided)"},
                        "name": {"type": "string", "description": "Name of the board"},
                        "desc": {"type": "string", "description": "Description of the board"},
                        "organization_id": {"type": "string", "description": "Organization ID (optional)"},
                        "default_lists": {"type": "boolean", "description": "Create default lists", "default": True},
                        "prefs": {
                            "type": "object",
                            "description": "Board preferences",
                            "properties": {
                                "permissionLevel": {"type": "string", "enum": ["private", "org", "public"]},
                                "voting": {"type": "string", "enum": ["disabled", "members", "observers", "org", "public"]},
                                "comments": {"type": "string", "enum": ["disabled", "members", "observers", "org", "public"]},
                                "background": {"type": "string", "description": "Board background"}
                            }
                        }
                    },
                    "required": ["name"]
                }
            },
            "update_board": {
                "description": "Update an existing board",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "api_key": {"type": "string", "description": "Trello API key (optional, will prompt if not provided)"},
                        "token": {"type": "string", "description": "Trello API token (optional, will prompt if not provided)"},
                        "board_id": {"type": "string", "description": "ID of the board to update"},
                        "name": {"type": "string", "description": "New name for the board"},
                        "desc": {"type": "string", "description": "New description for the board"},
                        "closed": {"type": "boolean", "description": "Whether the board is closed"},
                        "prefs": {
                            "type": "object",
                            "description": "Board preferences to update",
                            "properties": {
                                "permissionLevel": {"type": "string", "enum": ["private", "org", "public"]},
                                "voting": {"type": "string", "enum": ["disabled", "members", "observers", "org", "public"]},
                                "comments": {"type": "string", "enum": ["disabled", "members", "observers", "org", "public"]},
                                "background": {"type": "string", "description": "Board background"}
                            }
                        }
                    },
                    "required": ["board_id"]
                }
            },
            "get_lists": {
                "description": "Get all lists on a board",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "api_key": {"type": "string", "description": "Trello API key (optional, will prompt if not provided)"},
                        "token": {"type": "string", "description": "Trello API token (optional, will prompt if not provided)"},
                        "board_id": {"type": "string", "description": "ID of the board"}
                    },
                    "required": ["board_id"]
                }
            },
            "create_list": {
                "description": "Create a new list on a board",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "api_key": {"type": "string", "description": "Trello API key (optional, will prompt if not provided)"},
                        "token": {"type": "string", "description": "Trello API token (optional, will prompt if not provided)"},
                        "name": {"type": "string", "description": "Name of the list"},
                        "board_id": {"type": "string", "description": "ID of the board"},
                        "pos": {"type": ["string", "number"], "description": "Position of the list"}
                    },
                    "required": ["name", "board_id"]
                }
            },
            "get_cards": {
                "description": "Get cards from a board or list",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "api_key": {"type": "string", "description": "Trello API key (optional, will prompt if not provided)"},
                        "token": {"type": "string", "description": "Trello API token (optional, will prompt if not provided)"},
                        "board_id": {"type": "string", "description": "ID of the board (optional if list_id provided)"},
                        "list_id": {"type": "string", "description": "ID of the list (optional if board_id provided)"}
                    },
                    "required": [],
                    "oneOf": [
                        {"required": ["board_id"]},
                        {"required": ["list_id"]}
                    ]
                }
            },
            "create_card": {
                "description": "Create a new card",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "api_key": {"type": "string", "description": "Trello API key (optional, will prompt if not provided)"},
                        "token": {"type": "string", "description": "Trello API token (optional, will prompt if not provided)"},
                        "name": {"type": "string", "description": "Name of the card"},
                        "list_id": {"type": "string", "description": "ID of the list"},
                        "desc": {"type": "string", "description": "Description of the card"},
                        "pos": {"type": ["string", "number"], "description": "Position of the card"},
                        "due": {"type": "string", "description": "Due date (ISO format)"},
                        "labels": {
                            "type": "array",
                            "items": {"type": "string"},
                            "description": "Array of label IDs"
                        },
                        "members": {
                            "type": "array",
                            "items": {"type": "string"},
                            "description": "Array of member IDs"
                        }
                    },
                    "required": ["name", "list_id"]
                }
            },
            "update_card": {
                "description": "Update an existing card",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "api_key": {"type": "string", "description": "Trello API key (optional, will prompt if not provided)"},
                        "token": {"type": "string", "description": "Trello API token (optional, will prompt if not provided)"},
                        "card_id": {"type": "string", "description": "ID of the card to update"},
                        "name": {"type": "string", "description": "New name for the card"},
                        "desc": {"type": "string", "description": "New description for the card"},
                        "closed": {"type": "boolean", "description": "Whether the card is closed"},
                        "list_id": {"type": "string", "description": "Move card to this list ID"},
                        "pos": {"type": ["string", "number"], "description": "New position of the card"},
                        "due": {"type": "string", "description": "Due date (ISO format, null to remove)"}
                    },
                    "required": ["card_id"]
                }
            },
            "add_member_to_card": {
                "description": "Add a member to a card",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "api_key": {"type": "string", "description": "Trello API key (optional, will prompt if not provided)"},
                        "token": {"type": "string", "description": "Trello API token (optional, will prompt if not provided)"},
                        "card_id": {"type": "string", "description": "ID of the card"},
                        "member_id": {"type": "string", "description": "ID of the member to add"}
                    },
                    "required": ["card_id", "member_id"]
                }
            },
            "search_cards": {
                "description": "Search for cards across boards",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "api_key": {"type": "string", "description": "Trello API key (optional, will prompt if not provided)"},
                        "token": {"type": "string", "description": "Trello API token (optional, will prompt if not provided)"},
                        "query": {"type": "string", "description": "Search query"},
                        "board_ids": {
                            "type": "array",
                            "items": {"type": "string"},
                            "description": "Array of board IDs to search in (optional)"
                        },
                        "limit": {"type": "integer", "description": "Maximum number of results", "default": 50}
                    },
                    "required": ["query"]
                }
            }
        }
        
    async def execute_tool(self, tool_name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a tool with the given arguments"""
        try:
            # Get credentials: use provided or prompt user
            api_key = arguments.get("api_key")
            token = arguments.get("token")
            
            # If not provided, try to get from cache or prompt user
            if not api_key or not token:
                api_key, token = self.credential_manager.get_or_prompt_credentials(api_key, token)
            
            # Extract credentials
            credentials = TrelloCredentials(
                api_key=api_key,
                token=token
            )
            
            # Validate credentials
            validation_result = await self.get_client().validate_credentials(credentials)
            if not validation_result["valid"]:
                return {
                    "content": [{
                        "type": "text",
                        "text": f"❌ Invalid credentials: {validation_result['error']}"
                    }],
                    "isError": True
                }
            
            # Execute the specific tool
            if tool_name == "list_boards":
                return await self._list_boards(credentials)
            elif tool_name == "get_board":
                return await self._get_board(credentials, arguments)
            elif tool_name == "create_board":
                return await self._create_board(credentials, arguments)
            elif tool_name == "update_board":
                return await self._update_board(credentials, arguments)
            elif tool_name == "get_lists":
                return await self._get_lists(credentials, arguments)
            elif tool_name == "create_list":
                return await self._create_list(credentials, arguments)
            elif tool_name == "get_cards":
                return await self._get_cards(credentials, arguments)
            elif tool_name == "create_card":
                return await self._create_card(credentials, arguments)
            elif tool_name == "update_card":
                return await self._update_card(credentials, arguments)
            elif tool_name == "add_member_to_card":
                return await self._add_member_to_card(credentials, arguments)
            elif tool_name == "search_cards":
                return await self._search_cards(credentials, arguments)
            else:
                return {
                    "content": [{
                        "type": "text",
                        "text": f"❌ Unknown tool: {tool_name}"
                    }],
                    "isError": True
                }
                
        except Exception as e:
            logger.error(f"Tool execution failed: {e}")
            return {
                "content": [{
                    "type": "text",
                    "text": f"❌ Tool execution failed: {str(e)}"
                }],
                "isError": True
            }
            
    async def _list_boards(self, credentials: TrelloCredentials) -> Dict[str, Any]:
        """List all boards"""
        try:
            boards = await self.get_client().list_boards(credentials)
            
            if not boards:
                return {
                    "content": [{
                        "type": "text",
                        "text": "📋 No boards found"
                    }]
                }
                
            board_list = []
            for board in boards:
                board_info = f"• **{board.get('name', 'Unnamed')}** (`{board.get('id')}`)\n"
                board_info += f"  URL: {board.get('url', 'N/A')}\n"
                if board.get('desc'):
                    board_info += f"  Description: {board['desc'][:100]}...\n" if len(board['desc']) > 100 else f"  Description: {board['desc']}\n"
                board_list.append(board_info)
                
            result_text = f"📋 **Found {len(boards)} boards:**\n\n" + "\n".join(board_list)
            
            return {
                "content": [{
                    "type": "text",
                    "text": result_text
                }]
            }
            
        except TrelloAPIError as e:
            return {
                "content": [{
                    "type": "text",
                    "text": f"❌ Failed to list boards: {str(e)}"
                }],
                "isError": True
            }
            
    async def _get_board(self, credentials: TrelloCredentials, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Get detailed board information"""
        try:
            board_id = arguments.get("board_id")
            board = await self.get_client().get_board(credentials, board_id)
            
            result_text = f"📋 **Board: {board.get('name', 'Unnamed')}**\n\n"
            result_text += f"**ID:** `{board.get('id')}`\n"
            result_text += f"**URL:** {board.get('url', 'N/A')}\n"
            result_text += f"**Closed:** {'Yes' if board.get('closed') else 'No'}\n"
            
            if board.get('desc'):
                result_text += f"**Description:** {board['desc']}\n"
                
            # Lists
            lists = board.get('lists', [])
            if lists:
                result_text += f"\n**Lists ({len(lists)}):**\n"
                for lst in lists:
                    result_text += f"• {lst.get('name', 'Unnamed')} (`{lst.get('id')}`)\n"
                    
            # Cards
            cards = board.get('cards', [])
            if cards:
                result_text += f"\n**Cards ({len(cards)}):**\n"
                for card in cards[:10]:  # Limit to first 10
                    result_text += f"• {card.get('name', 'Unnamed')} (`{card.get('id')}`)\n"
                if len(cards) > 10:
                    result_text += f"... and {len(cards) - 10} more cards\n"
                    
            # Members
            members = board.get('members', [])
            if members:
                result_text += f"\n**Members ({len(members)}):**\n"
                for member in members:
                    result_text += f"• {member.get('fullName', member.get('username', 'Unknown'))} (`{member.get('id')}`)\n"
                    
            return {
                "content": [{
                    "type": "text",
                    "text": result_text
                }]
            }
            
        except TrelloAPIError as e:
            return {
                "content": [{
                    "type": "text", 
                    "text": f"❌ Failed to get board: {str(e)}"
                }],
                "isError": True
            }
            
    async def _create_board(self, credentials: TrelloCredentials, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new board"""
        try:
            request = CreateBoardRequest(
                name=arguments.get("name"),
                desc=arguments.get("desc"),
                organization_id=arguments.get("organization_id"),
                default_lists=arguments.get("default_lists", True),
                prefs=arguments.get("prefs")
            )
            
            board = await self.get_client().create_board(credentials, request)
            
            result_text = f"✅ **Board created successfully!**\n\n"
            result_text += f"**Name:** {board.get('name')}\n"
            result_text += f"**ID:** `{board.get('id')}`\n"
            result_text += f"**URL:** {board.get('url')}\n"
            
            if board.get('desc'):
                result_text += f"**Description:** {board['desc']}\n"
                
            return {
                "content": [{
                    "type": "text",
                    "text": result_text
                }]
            }
            
        except TrelloAPIError as e:
            return {
                "content": [{
                    "type": "text",
                    "text": f"❌ Failed to create board: {str(e)}"
                }],
                "isError": True
            }
            
    async def _update_board(self, credentials: TrelloCredentials, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Update an existing board"""
        try:
            board_id = arguments.get("board_id")
            request = UpdateBoardRequest(
                name=arguments.get("name"),
                desc=arguments.get("desc"),
                closed=arguments.get("closed"),
                prefs=arguments.get("prefs")
            )
            
            board = await self.get_client().update_board(credentials, board_id, request)
            
            result_text = f"✅ **Board updated successfully!**\n\n"
            result_text += f"**Name:** {board.get('name')}\n"
            result_text += f"**ID:** `{board.get('id')}`\n"
            result_text += f"**URL:** {board.get('url')}\n"
            result_text += f"**Closed:** {'Yes' if board.get('closed') else 'No'}\n"
            
            return {
                "content": [{
                    "type": "text",
                    "text": result_text
                }]
            }
            
        except TrelloAPIError as e:
            return {
                "content": [{
                    "type": "text",
                    "text": f"❌ Failed to update board: {str(e)}"
                }],
                "isError": True
            }
            
    async def _get_lists(self, credentials: TrelloCredentials, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Get all lists on a board"""
        try:
            board_id = arguments.get("board_id")
            lists = await self.get_client().get_lists(credentials, board_id)
            
            if not lists:
                return {
                    "content": [{
                        "type": "text",
                        "text": f"📝 No lists found on board `{board_id}`"
                    }]
                }
                
            list_info = []
            for lst in lists:
                info = f"• **{lst.get('name', 'Unnamed')}** (`{lst.get('id')}`)\n"
                info += f"  Position: {lst.get('pos', 'N/A')}\n"
                info += f"  Closed: {'Yes' if lst.get('closed') else 'No'}\n"
                list_info.append(info)
                
            result_text = f"📝 **Found {len(lists)} lists:**\n\n" + "\n".join(list_info)
            
            return {
                "content": [{
                    "type": "text",
                    "text": result_text
                }]
            }
            
        except TrelloAPIError as e:
            return {
                "content": [{
                    "type": "text",
                    "text": f"❌ Failed to get lists: {str(e)}"
                }],
                "isError": True
            }
            
    async def _create_list(self, credentials: TrelloCredentials, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new list"""
        try:
            request = CreateListRequest(
                name=arguments.get("name"),
                board_id=arguments.get("board_id"),
                pos=arguments.get("pos")
            )
            
            lst = await self.get_client().create_list(credentials, request)
            
            result_text = f"✅ **List created successfully!**\n\n"
            result_text += f"**Name:** {lst.get('name')}\n"
            result_text += f"**ID:** `{lst.get('id')}`\n"
            result_text += f"**Board ID:** `{lst.get('idBoard')}`\n"
            result_text += f"**Position:** {lst.get('pos', 'N/A')}\n"
            
            return {
                "content": [{
                    "type": "text",
                    "text": result_text
                }]
            }
            
        except TrelloAPIError as e:
            return {
                "content": [{
                    "type": "text",
                    "text": f"❌ Failed to create list: {str(e)}"
                }],
                "isError": True
            }
            
    async def _get_cards(self, credentials: TrelloCredentials, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Get cards from a board or list"""
        try:
            board_id = arguments.get("board_id")
            list_id = arguments.get("list_id")
            
            cards = await self.get_client().get_cards(credentials, board_id, list_id)
            
            source = f"list `{list_id}`" if list_id else f"board `{board_id}`"
            
            if not cards:
                return {
                    "content": [{
                        "type": "text",
                        "text": f"🃏 No cards found in {source}"
                    }]
                }
                
            card_info = []
            for card in cards:
                info = f"• **{card.get('name', 'Unnamed')}** (`{card.get('id')}`)\n"
                if card.get('desc'):
                    desc_preview = card['desc'][:100] + "..." if len(card['desc']) > 100 else card['desc']
                    info += f"  Description: {desc_preview}\n"
                info += f"  URL: {card.get('url', 'N/A')}\n"
                if card.get('due'):
                    info += f"  Due: {card['due']}\n"
                if card.get('labels'):
                    label_names = [label.get('name', 'Unnamed') for label in card['labels']]
                    info += f"  Labels: {', '.join(label_names)}\n"
                card_info.append(info)
                
            result_text = f"🃏 **Found {len(cards)} cards in {source}:**\n\n" + "\n".join(card_info)
            
            return {
                "content": [{
                    "type": "text", 
                    "text": result_text
                }]
            }
            
        except TrelloAPIError as e:
            return {
                "content": [{
                    "type": "text",
                    "text": f"❌ Failed to get cards: {str(e)}"
                }],
                "isError": True
            }
            
    async def _create_card(self, credentials: TrelloCredentials, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new card"""
        try:
            from datetime import datetime
            
            # Parse due date if provided
            due_date = None
            if arguments.get("due"):
                try:
                    due_date = datetime.fromisoformat(arguments["due"].replace('Z', '+00:00'))
                except ValueError:
                    return {
                        "content": [{
                            "type": "text",
                            "text": "❌ Invalid due date format. Use ISO format (e.g., 2024-01-01T12:00:00Z)"
                        }],
                        "isError": True
                    }
                    
            request = CreateCardRequest(
                name=arguments.get("name"),
                list_id=arguments.get("list_id"),
                desc=arguments.get("desc"),
                pos=arguments.get("pos"),
                due=due_date,
                labels=arguments.get("labels"),
                members=arguments.get("members")
            )
            
            card = await self.get_client().create_card(credentials, request)
            
            result_text = f"✅ **Card created successfully!**\n\n"
            result_text += f"**Name:** {card.get('name')}\n"
            result_text += f"**ID:** `{card.get('id')}`\n"
            result_text += f"**List ID:** `{card.get('idList')}`\n"
            result_text += f"**URL:** {card.get('url')}\n"
            
            if card.get('desc'):
                result_text += f"**Description:** {card['desc']}\n"
            if card.get('due'):
                result_text += f"**Due:** {card['due']}\n"
                
            return {
                "content": [{
                    "type": "text",
                    "text": result_text
                }]
            }
            
        except TrelloAPIError as e:
            return {
                "content": [{
                    "type": "text",
                    "text": f"❌ Failed to create card: {str(e)}"
                }],
                "isError": True
            }
            
    async def _update_card(self, credentials: TrelloCredentials, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Update an existing card"""
        try:
            from datetime import datetime
            
            card_id = arguments.get("card_id")
            
            # Parse due date if provided
            due_date = None
            if "due" in arguments:
                if arguments["due"] is None or arguments["due"] == "":
                    due_date = None  # Remove due date
                else:
                    try:
                        due_date = datetime.fromisoformat(arguments["due"].replace('Z', '+00:00'))
                    except ValueError:
                        return {
                            "content": [{
                                "type": "text",
                                "text": "❌ Invalid due date format. Use ISO format (e.g., 2024-01-01T12:00:00Z) or null to remove"
                            }],
                            "isError": True
                        }
                        
            request = UpdateCardRequest(
                name=arguments.get("name"),
                desc=arguments.get("desc"),
                closed=arguments.get("closed"),
                list_id=arguments.get("list_id"),
                pos=arguments.get("pos"),
                due=due_date
            )
            
            card = await self.get_client().update_card(credentials, card_id, request)
            
            result_text = f"✅ **Card updated successfully!**\n\n"
            result_text += f"**Name:** {card.get('name')}\n"
            result_text += f"**ID:** `{card.get('id')}`\n"
            result_text += f"**List ID:** `{card.get('idList')}`\n"
            result_text += f"**URL:** {card.get('url')}\n"
            result_text += f"**Closed:** {'Yes' if card.get('closed') else 'No'}\n"
            
            return {
                "content": [{
                    "type": "text",
                    "text": result_text
                }]
            }
            
        except TrelloAPIError as e:
            return {
                "content": [{
                    "type": "text",
                    "text": f"❌ Failed to update card: {str(e)}"
                }],
                "isError": True
            }
            
    async def _add_member_to_card(self, credentials: TrelloCredentials, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Add a member to a card"""
        try:
            card_id = arguments.get("card_id")
            member_id = arguments.get("member_id")
            
            result = await self.get_client().add_member_to_card(credentials, card_id, member_id)
            
            result_text = f"✅ **Member added to card successfully!**\n\n"
            result_text += f"**Card ID:** `{card_id}`\n"
            result_text += f"**Member ID:** `{member_id}`\n"
            
            return {
                "content": [{
                    "type": "text",
                    "text": result_text
                }]
            }
            
        except TrelloAPIError as e:
            return {
                "content": [{
                    "type": "text",
                    "text": f"❌ Failed to add member to card: {str(e)}"
                }],
                "isError": True
            }
            
    async def _search_cards(self, credentials: TrelloCredentials, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Search for cards"""
        try:
            request = SearchRequest(
                query=arguments.get("query"),
                board_ids=arguments.get("board_ids"),
                limit=arguments.get("limit", 50)
            )
            
            cards = await self.get_client().search_cards(credentials, request)
            
            if not cards:
                return {
                    "content": [{
                        "type": "text",
                        "text": f"🔍 No cards found for query: '{request.query}'"
                    }]
                }
                
            card_info = []
            for card in cards:
                info = f"• **{card.get('name', 'Unnamed')}** (`{card.get('id')}`)\n"
                if card.get('desc'):
                    desc_preview = card['desc'][:100] + "..." if len(card['desc']) > 100 else card['desc']
                    info += f"  Description: {desc_preview}\n"
                info += f"  URL: {card.get('url', 'N/A')}\n"
                if card.get('due'):
                    info += f"  Due: {card['due']}\n"
                card_info.append(info)
                
            result_text = f"🔍 **Found {len(cards)} cards for '{request.query}':**\n\n" + "\n".join(card_info)
            
            return {
                "content": [{
                    "type": "text",
                    "text": result_text
                }]
            }
            
        except TrelloAPIError as e:
            return {
                "content": [{
                    "type": "text",
                    "text": f"❌ Failed to search cards: {str(e)}"
                }],
                "isError": True
            }
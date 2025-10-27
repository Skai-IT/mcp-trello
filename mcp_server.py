"""
Trello MCP Server - MCP Protocol Implementation

This module implements the Model Context Protocol for Trello integration.
Handles initialization, tool registration, and request routing.
"""

import asyncio
import logging
from typing import Any, Dict, List, Optional

from config import config
from tools import TrelloTools

logger = logging.getLogger(__name__)


class TrelloMCPServer:
    """MCP Server implementation for Trello integration"""
    
    def __init__(self):
        self.tools = None
        self.initialized = False
        self.capabilities = {
            "tools": {},
            "resources": {},
            "prompts": {}
        }
        
    async def initialize(self):
        """Initialize the MCP server"""
        try:
            logger.info("Initializing Trello MCP Server...")
            
            # Initialize tools
            self.tools = TrelloTools()
            
            # Set capabilities
            self.capabilities = {
                "tools": {
                    "listChanged": False
                },
                "resources": {},
                "prompts": {}
            }
            
            self.initialized = True
            logger.info("MCP Server initialization complete")
            
        except Exception as e:
            logger.error(f"Failed to initialize MCP server: {e}")
            raise
            
    async def cleanup(self):
        """Cleanup server resources"""
        logger.info("Cleaning up MCP server resources...")
        self.initialized = False
        
    def get_available_tools(self) -> List[Dict[str, Any]]:
        """Get list of available tools"""
        if not self.tools:
            return []
            
        return [
            {
                "name": name,
                "description": tool_info.get("description", ""),
                "inputSchema": tool_info.get("inputSchema", {})
            }
            for name, tool_info in self.tools.get_tools().items()
        ]
        
    async def handle_request(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Handle MCP protocol requests"""
        try:
            method = request.get("method")
            params = request.get("params", {})
            request_id = request.get("id")
            
            logger.info(f"Handling MCP request: {method}")
            
            if method == "initialize":
                return await self._handle_initialize(request_id, params)
            elif method == "tools/list":
                return await self._handle_tools_list(request_id)
            elif method == "tools/call":
                return await self._handle_tool_call(request_id, params)
            elif method == "resources/list":
                return await self._handle_resources_list(request_id)
            elif method == "prompts/list":
                return await self._handle_prompts_list(request_id)
            else:
                return self._create_error_response(
                    request_id, -32601, f"Method not found: {method}"
                )
                
        except Exception as e:
            logger.error(f"Error handling MCP request: {e}")
            return self._create_error_response(
                request.get("id"), -32603, f"Internal error: {str(e)}"
            )
            
    async def _handle_initialize(self, request_id: Optional[str], params: Dict[str, Any]) -> Dict[str, Any]:
        """Handle initialize request"""
        try:
            protocol_version = params.get("protocolVersion")
            client_info = params.get("clientInfo", {})
            
            logger.info(f"Initialize request from client: {client_info}")
            
            # Validate protocol version
            supported_versions = ["2024-11-05"]
            if protocol_version not in supported_versions:
                return self._create_error_response(
                    request_id, -32602, 
                    f"Unsupported protocol version: {protocol_version}"
                )
                
            response = {
                "jsonrpc": "2.0",
                "id": request_id,
                "result": {
                    "protocolVersion": protocol_version,
                    "capabilities": self.capabilities,
                    "serverInfo": {
                        "name": "trello-mcp",
                        "version": "1.0.0"
                    }
                }
            }
            
            logger.info("Initialize request completed successfully")
            return response
            
        except Exception as e:
            logger.error(f"Initialize request failed: {e}")
            return self._create_error_response(request_id, -32603, str(e))
            
    async def _handle_tools_list(self, request_id: Optional[str]) -> Dict[str, Any]:
        """Handle tools/list request"""
        try:
            if not self.tools:
                tools_list = []
            else:
                tools_dict = self.tools.get_tools()
                tools_list = [
                    {
                        "name": name,
                        "description": info["description"],
                        "inputSchema": info["inputSchema"]
                    }
                    for name, info in tools_dict.items()
                ]
                
            response = {
                "jsonrpc": "2.0",
                "id": request_id,
                "result": {
                    "tools": tools_list
                }
            }
            
            logger.info(f"Tools list request completed: {len(tools_list)} tools")
            return response
            
        except Exception as e:
            logger.error(f"Tools list request failed: {e}")
            return self._create_error_response(request_id, -32603, str(e))
            
    async def _handle_tool_call(self, request_id: Optional[str], params: Dict[str, Any]) -> Dict[str, Any]:
        """Handle tools/call request"""
        try:
            tool_name = params.get("name")
            arguments = params.get("arguments", {})
            
            if not tool_name:
                return self._create_error_response(
                    request_id, -32602, "Tool name is required"
                )
                
            if not self.tools:
                return self._create_error_response(
                    request_id, -32603, "Tools not initialized"
                )
                
            logger.info(f"Executing tool: {tool_name}")
            result = await self.tools.execute_tool(tool_name, arguments)
            
            response = {
                "jsonrpc": "2.0",
                "id": request_id,
                "result": result
            }
            
            logger.info(f"Tool execution completed: {tool_name}")
            return response
            
        except Exception as e:
            logger.error(f"Tool call failed: {e}")
            return self._create_error_response(request_id, -32603, str(e))
            
    async def _handle_resources_list(self, request_id: Optional[str]) -> Dict[str, Any]:
        """Handle resources/list request"""
        response = {
            "jsonrpc": "2.0",
            "id": request_id,
            "result": {
                "resources": []
            }
        }
        return response
        
    async def _handle_prompts_list(self, request_id: Optional[str]) -> Dict[str, Any]:
        """Handle prompts/list request"""
        response = {
            "jsonrpc": "2.0",
            "id": request_id,
            "result": {
                "prompts": []
            }
        }
        return response
        
    def _create_error_response(self, request_id: Optional[str], code: int, message: str) -> Dict[str, Any]:
        """Create error response"""
        return {
            "jsonrpc": "2.0",
            "id": request_id,
            "error": {
                "code": code,
                "message": message
            }
        }
#!/usr/bin/env python3
"""
Trello MCP Server - HTTP Server for Google Cloud Run

This module provides an HTTP wrapper around the MCP server for Cloud Run deployment.
Handles health checks, request routing, and graceful shutdown.
"""

import asyncio
import json
import logging
import os
import signal
import sys
from contextlib import asynccontextmanager
from typing import Any, Dict

import uvicorn
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from config import config
from logging_config import setup_logging
from mcp_server import TrelloMCPServer

# Setup logging
logger = setup_logging()

# Global MCP server instance
mcp_server = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage application lifespan - startup and shutdown"""
    global mcp_server
    
    try:
        # Startup - Initialize server quickly to respond to health checks
        logger.info("Starting Trello MCP Server...")
        mcp_server = TrelloMCPServer()
        
        # Initialize tools asynchronously in background to not block startup
        try:
            await mcp_server.initialize()
            logger.info("MCP Server initialized successfully")
        except Exception as e:
            logger.warning(f"MCP server initialization warning: {e}")
            # Don't fail startup - health check will still work
        
        yield
        
    except Exception as e:
        logger.error(f"Failed to start MCP server: {e}")
        # Don't re-raise - allow server to start even if initialization fails
    finally:
        # Shutdown
        logger.info("Shutting down Trello MCP Server...")
        if mcp_server:
            await mcp_server.cleanup()
        logger.info("Server shutdown complete")


# Create FastAPI app with lifespan management
app = FastAPI(
    title="Trello MCP Server",
    description="Model Context Protocol server for Trello API integration",
    version="1.0.0",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
async def health_check():
    """Health check endpoint for Cloud Run"""
    try:
        status = {
            "status": "healthy",
            "service": "trello-mcp",
            "version": "1.0.0",
            "timestamp": config.get_timestamp()
        }
        
        # Additional health checks
        if mcp_server:
            status["mcp_server"] = "initialized"
            status["tools_count"] = len(mcp_server.get_available_tools())
        else:
            status["mcp_server"] = "not_initialized"
            status["tools_count"] = 0
            
        logger.info(f"Health check: {status}")
        return JSONResponse(status_code=200, content=status)
        
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        error_status = {
            "status": "unhealthy",
            "error": str(e),
            "timestamp": config.get_timestamp()
        }
        return JSONResponse(status_code=500, content=error_status)


@app.get("/")
async def root():
    """Root endpoint with server information"""
    return {
        "name": "Trello MCP Server",
        "description": "Model Context Protocol server for Trello API integration",
        "version": "1.0.0",
        "endpoints": {
            "health": "/health",
            "login": "/auth/login (GET)",
            "mcp": "/mcp (POST)",
            "tools": "/tools (GET)"
        },
        "features": {
            "interactive_login": True,
            "session_credentials_caching": True,
            "no_persistent_storage": True
        },
        "documentation": "https://github.com/Skai-IT/trello-mcp-server"
    }


@app.get("/tools")
async def list_tools():
    """List available MCP tools"""
    try:
        if not mcp_server:
            raise HTTPException(status_code=503, detail="MCP server not initialized")
            
        tools = mcp_server.get_available_tools()
        return {
            "tools": tools,
            "count": len(tools),
            "timestamp": config.get_timestamp()
        }
        
    except Exception as e:
        logger.error(f"Failed to list tools: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/auth/login")
async def get_login_url():
    """Get Trello login URL for authentication"""
    return {
        "message": "Interactive login will be triggered on first tool call",
        "login_url": "https://trello.com/app-key",
        "instructions": {
            "step_1": "Visit https://trello.com/app-key",
            "step_2": "Copy your API Key",
            "step_3": "Click 'Token' link to generate/view your token",
            "step_4": "When prompted by the MCP server, paste both values"
        },
        "features": {
            "automatic_browser_open": True,
            "session_caching": True,
            "cache_duration_minutes": 480,
            "no_disk_storage": True
        }
    }


@app.post("/mcp")
async def handle_mcp_request(request: Request):
    """Handle MCP protocol requests"""
    try:
        if not mcp_server:
            raise HTTPException(status_code=503, detail="MCP server not initialized")
            
        # Get request body
        body = await request.body()
        if not body:
            raise HTTPException(status_code=400, detail="Request body is required")
            
        try:
            request_data = json.loads(body)
        except json.JSONDecodeError as e:
            raise HTTPException(status_code=400, detail=f"Invalid JSON: {e}")
            
        # Validate JSON-RPC structure
        if not isinstance(request_data, dict):
            raise HTTPException(status_code=400, detail="Request must be a JSON object")
            
        if "jsonrpc" not in request_data or request_data["jsonrpc"] != "2.0":
            raise HTTPException(status_code=400, detail="Invalid JSON-RPC version")
            
        if "method" not in request_data:
            raise HTTPException(status_code=400, detail="Method is required")
            
        # Process MCP request
        logger.info(f"Processing MCP request: {request_data.get('method')}")
        response = await mcp_server.handle_request(request_data)
        
        logger.info(f"MCP response generated for method: {request_data.get('method')}")
        return response
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"MCP request failed: {e}")
        
        # Return JSON-RPC error response
        error_response = {
            "jsonrpc": "2.0",
            "error": {
                "code": -32603,
                "message": "Internal error",
                "data": str(e)
            },
            "id": request_data.get("id") if 'request_data' in locals() else None
        }
        
        return JSONResponse(status_code=500, content=error_response)


def signal_handler(signum, frame):
    """Handle shutdown signals"""
    logger.info(f"Received signal {signum}, shutting down...")
    sys.exit(0)


def main():
    """Main entry point"""
    # Setup signal handlers
    signal.signal(signal.SIGTERM, signal_handler)
    signal.signal(signal.SIGINT, signal_handler)
    
    # Get port from environment
    port = int(os.getenv("PORT", 8080))
    
    logger.info(f"Starting Trello MCP Server on port {port}")
    
    # Run the server
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=port,
        log_level="info" if config.DEBUG else "warning",
        access_log=config.DEBUG
    )


if __name__ == "__main__":
    main()
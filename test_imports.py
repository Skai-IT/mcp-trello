#!/usr/bin/env python3
"""
Test script to verify Trello MCP Server components

This script validates that all modules can be imported and that all 11 tools
are properly registered and available.
"""

import sys
import asyncio
from typing import List


def test_imports():
    """Test that all required modules can be imported"""
    print("🧪 Testing module imports...")
    
    try:
        # Test core imports
        import main
        print("✅ main.py imported successfully")
        
        import mcp_server
        print("✅ mcp_server.py imported successfully")
        
        import trello_client
        print("✅ trello_client.py imported successfully")
        
        import tools
        print("✅ tools.py imported successfully")
        
        import schemas
        print("✅ schemas.py imported successfully")
        
        import config
        print("✅ config.py imported successfully")
        
        import logging_config
        print("✅ logging_config.py imported successfully")
        
        return True
        
    except ImportError as e:
        print(f"❌ Import failed: {e}")
        return False


def test_tool_registration():
    """Test that all 11 tools are properly registered"""
    print("\n🛠️ Testing tool registration...")
    
    try:
        from tools import TrelloTools
        
        # Initialize tools
        tools_instance = TrelloTools()
        available_tools = tools_instance.get_tools()
        
        print(f"✅ TrelloTools initialized successfully")
        print(f"✅ {len(available_tools)} tools registered")
        
        # Expected tools
        expected_tools = [
            "list_boards",
            "get_board", 
            "create_board",
            "update_board",
            "get_lists",
            "create_list",
            "get_cards",
            "create_card",
            "update_card", 
            "add_member_to_card",
            "search_cards"
        ]
        
        # Check each expected tool
        missing_tools = []
        for tool_name in expected_tools:
            if tool_name in available_tools:
                print(f"✅ {tool_name}")
            else:
                print(f"❌ {tool_name} - MISSING")
                missing_tools.append(tool_name)
        
        # Check for unexpected tools
        unexpected_tools = []
        for tool_name in available_tools:
            if tool_name not in expected_tools:
                unexpected_tools.append(tool_name)
                
        if unexpected_tools:
            print(f"\n⚠️ Unexpected tools found: {unexpected_tools}")
            
        if missing_tools:
            print(f"\n❌ Missing tools: {missing_tools}")
            return False
        elif len(available_tools) != len(expected_tools):
            print(f"\n❌ Tool count mismatch: expected {len(expected_tools)}, got {len(available_tools)}")
            return False
        else:
            print(f"\n✅ All {len(expected_tools)} tools registered correctly")
            return True
            
    except Exception as e:
        print(f"❌ Tool registration test failed: {e}")
        return False


def test_schemas():
    """Test that Pydantic schemas are working"""
    print("\n📋 Testing Pydantic schemas...")
    
    try:
        from schemas import TrelloCredentials, CreateBoardRequest, CreateCardRequest
        
        # Test credential validation
        try:
            creds = TrelloCredentials(api_key="test_key", token="test_token")
            print("✅ TrelloCredentials validation working")
        except Exception as e:
            print(f"❌ TrelloCredentials validation failed: {e}")
            return False
            
        # Test board request validation  
        try:
            board_req = CreateBoardRequest(name="Test Board")
            print("✅ CreateBoardRequest validation working")
        except Exception as e:
            print(f"❌ CreateBoardRequest validation failed: {e}")
            return False
            
        # Test card request validation
        try:
            card_req = CreateCardRequest(name="Test Card", list_id="test_list")
            print("✅ CreateCardRequest validation working")
        except Exception as e:
            print(f"❌ CreateCardRequest validation failed: {e}")
            return False
            
        return True
        
    except Exception as e:
        print(f"❌ Schema test failed: {e}")
        return False


def test_server_initialization():
    """Test that the MCP server can be initialized"""
    print("\n🚀 Testing MCP server initialization...")
    
    try:
        from mcp_server import TrelloMCPServer
        
        # Initialize server
        server = TrelloMCPServer()
        print("✅ TrelloMCPServer created successfully")
        
        # Check initial state
        if not server.initialized:
            print("✅ Server starts in uninitialized state")
        else:
            print("❌ Server should start uninitialized")
            return False
            
        return True
        
    except Exception as e:
        print(f"❌ Server initialization test failed: {e}")
        return False


async def test_async_functionality():
    """Test async functionality without making real API calls"""
    print("\n⚡ Testing async functionality...")
    
    try:
        from trello_client import TrelloClient, RateLimiter
        
        # Test rate limiter
        rate_limiter = RateLimiter(max_requests=5, time_window=10)
        print("✅ RateLimiter created successfully")
        
        # Test that we can acquire rate limit permission
        await rate_limiter.acquire()
        print("✅ Rate limiter acquire() works")
        
        # Test client creation
        client = TrelloClient()
        print("✅ TrelloClient created successfully")
        
        return True
        
    except Exception as e:
        print(f"❌ Async functionality test failed: {e}")
        return False


def test_configuration():
    """Test configuration loading"""
    print("\n⚙️ Testing configuration...")
    
    try:
        from config import config
        
        # Test that config values are accessible
        port = config.PORT
        debug = config.DEBUG
        service_name = config.SERVICE_NAME
        
        print(f"✅ Configuration loaded: PORT={port}, DEBUG={debug}")
        print(f"✅ Service name: {service_name}")
        
        # Test utility functions
        timestamp = config.get_timestamp()
        is_cloud_run = config.is_cloud_run()
        
        print(f"✅ Timestamp function works: {timestamp[:19]}...")
        print(f"✅ Cloud Run detection: {is_cloud_run}")
        
        return True
        
    except Exception as e:
        print(f"❌ Configuration test failed: {e}")
        return False


def print_summary(results: List[bool]):
    """Print test summary"""
    passed = sum(results)
    total = len(results)
    
    print("\n" + "="*60)
    print("🎯 TEST SUMMARY")
    print("="*60)
    
    if passed == total:
        print(f"🎉 ALL TESTS PASSED! ({passed}/{total})")
        print("\n✅ Your Trello MCP Server is ready for deployment!")
        print("\nNext steps:")
        print("1. Read QUICKSTART.md for deployment instructions")
        print("2. Get your Trello API credentials")
        print("3. Deploy to Google Cloud Run")
        print("4. Integrate with your AI agent")
    else:
        print(f"❌ SOME TESTS FAILED ({passed}/{total} passed)")
        print("\n🔧 Please fix the issues above before deploying.")
        print("Check that all dependencies are installed:")
        print("  pip install -r requirements.txt")


async def main():
    """Run all tests"""
    print("🚀 Trello MCP Server - Component Verification")
    print("="*60)
    
    # Run all tests
    results = [
        test_imports(),
        test_tool_registration(), 
        test_schemas(),
        test_server_initialization(),
        await test_async_functionality(),
        test_configuration()
    ]
    
    print_summary(results)
    
    # Exit with appropriate code
    if all(results):
        sys.exit(0)
    else:
        sys.exit(1)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\n⚠️ Test interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n💥 Unexpected error during testing: {e}")
        sys.exit(1)
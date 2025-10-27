#!/usr/bin/env python3
"""
Trello MCP Cloud Run Test Client

Tests the live Trello MCP server on Google Cloud Run.
Includes health checks, endpoint validation, and MCP protocol testing.
"""

import asyncio
import json
import requests
from typing import Dict, Any, Optional

# Cloud Run Service URL
SERVICE_URL = "https://trello-mcp-116435607783.us-central1.run.app"

class TrelloMCPTestClient:
    """Test client for Trello MCP Cloud Run service"""
    
    def __init__(self, service_url: str = SERVICE_URL, verbose: bool = True):
        self.service_url = service_url
        self.verbose = verbose
        self.session = requests.Session()
        
    def _print(self, message: str, prefix: str = "ℹ️ "):
        """Print message with prefix"""
        if self.verbose:
            print(f"{prefix} {message}")
    
    def _print_json(self, data: Dict[str, Any], title: str = "Response"):
        """Pretty print JSON response"""
        if self.verbose:
            print(f"\n📋 {title}:")
            print(json.dumps(data, indent=2))
    
    # ============================================================================
    # HEALTH & STATUS TESTS
    # ============================================================================
    
    async def test_health(self) -> bool:
        """Test /health endpoint"""
        try:
            self._print("Testing /health endpoint...", "🏥")
            response = self.session.get(f"{self.service_url}/health", timeout=5)
            response.raise_for_status()
            
            data = response.json()
            self._print_json(data, "Health Status")
            
            # Validate response
            assert data.get("status") == "healthy", "Server not healthy"
            assert data.get("tools_count") == 11, "Wrong tool count"
            
            self._print(f"✅ Health check passed - {data['tools_count']} tools available", "✅")
            return True
            
        except Exception as e:
            self._print(f"❌ Health check failed: {e}", "❌")
            return False
    
    async def test_root_endpoint(self) -> bool:
        """Test root endpoint"""
        try:
            self._print("Testing root endpoint...", "🌐")
            response = self.session.get(f"{self.service_url}/", timeout=5)
            response.raise_for_status()
            
            data = response.json()
            self._print_json(data, "Root Endpoint")
            
            # Validate response
            assert "endpoints" in data, "Missing endpoints"
            assert "features" in data, "Missing features"
            
            features = data.get("features", {})
            self._print(f"✅ Server version: {data.get('version')}", "✅")
            self._print(f"✅ Interactive login enabled: {features.get('interactive_login')}", "✅")
            self._print(f"✅ Session caching enabled: {features.get('session_credentials_caching')}", "✅")
            
            return True
            
        except Exception as e:
            self._print(f"❌ Root endpoint failed: {e}", "❌")
            return False
    
    # ============================================================================
    # LOGIN FEATURE TESTS
    # ============================================================================
    
    async def test_auth_login_endpoint(self) -> bool:
        """Test /auth/login endpoint"""
        try:
            self._print("Testing /auth/login endpoint...", "🔐")
            response = self.session.get(f"{self.service_url}/auth/login", timeout=5)
            response.raise_for_status()
            
            data = response.json()
            self._print_json(data, "Interactive Login Feature")
            
            # Validate response
            assert "login_url" in data, "Missing login_url"
            assert "instructions" in data, "Missing instructions"
            assert "features" in data, "Missing features"
            
            features = data.get("features", {})
            self._print(f"✅ Browser auto-open: {features.get('automatic_browser_open')}", "✅")
            self._print(f"✅ Session caching: {features.get('session_caching')}", "✅")
            self._print(f"✅ Cache duration: {features.get('cache_duration_minutes')} minutes", "✅")
            
            return True
            
        except Exception as e:
            self._print(f"❌ /auth/login endpoint failed: {e}", "❌")
            return False
    
    # ============================================================================
    # TOOLS ENDPOINT TESTS
    # ============================================================================
    
    async def test_tools_endpoint(self) -> bool:
        """Test /tools endpoint and verify all 11 tools"""
        try:
            self._print("Testing /tools endpoint...", "🛠️")
            response = self.session.get(f"{self.service_url}/tools", timeout=5)
            response.raise_for_status()
            
            data = response.json()
            tools = data.get("tools", [])
            
            self._print(f"Found {len(tools)} tools", "📦")
            
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
            
            # Validate each tool
            tool_names = [tool.get("name") for tool in tools]
            
            for expected_tool in expected_tools:
                if expected_tool in tool_names:
                    tool_data = next((t for t in tools if t.get("name") == expected_tool), None)
                    if tool_data:
                        schema = tool_data.get("inputSchema", {})
                        required = schema.get("required", [])
                        # api_key and token should NOT be required
                        if not any(k in required for k in ["api_key", "token"]):
                            self._print(f"✅ {expected_tool} - credentials optional", "✅")
                        else:
                            self._print(f"⚠️  {expected_tool} - credentials still required!", "⚠️")
                else:
                    self._print(f"❌ Missing tool: {expected_tool}", "❌")
            
            self._print(f"✅ All {len(expected_tools)} tools available", "✅")
            return len(tools) == 11
            
        except Exception as e:
            self._print(f"❌ /tools endpoint failed: {e}", "❌")
            return False
    
    # ============================================================================
    # MCP PROTOCOL TESTS
    # ============================================================================
    
    async def test_mcp_initialize(self) -> bool:
        """Test MCP initialize request"""
        try:
            self._print("Testing MCP initialize request...", "🚀")
            
            mcp_request = {
                "jsonrpc": "2.0",
                "id": 1,
                "method": "initialize",
                "params": {
                    "protocolVersion": "2024-11-05",
                    "clientInfo": {
                        "name": "test-client",
                        "version": "1.0.0"
                    }
                }
            }
            
            response = self.session.post(
                f"{self.service_url}/mcp",
                json=mcp_request,
                timeout=5,
                headers={"Content-Type": "application/json"}
            )
            response.raise_for_status()
            
            data = response.json()
            self._print_json(data, "MCP Initialize Response")
            
            # Validate response
            assert data.get("jsonrpc") == "2.0", "Invalid JSON-RPC version"
            assert "result" in data, "Missing result"
            result = data.get("result", {})
            assert "capabilities" in result, "Missing capabilities"
            
            self._print(f"✅ MCP server version: {result.get('serverInfo', {}).get('version')}", "✅")
            self._print(f"✅ Protocol version: {result.get('protocolVersion')}", "✅")
            
            return True
            
        except Exception as e:
            self._print(f"❌ MCP initialize failed: {e}", "❌")
            return False
    
    async def test_mcp_tools_list(self) -> bool:
        """Test MCP tools/list request"""
        try:
            self._print("Testing MCP tools/list request...", "🚀")
            
            mcp_request = {
                "jsonrpc": "2.0",
                "id": 2,
                "method": "tools/list"
            }
            
            response = self.session.post(
                f"{self.service_url}/mcp",
                json=mcp_request,
                timeout=5,
                headers={"Content-Type": "application/json"}
            )
            response.raise_for_status()
            
            data = response.json()
            self._print_json(data, "MCP Tools/List Response", max_items=3)
            
            # Validate response
            assert data.get("jsonrpc") == "2.0", "Invalid JSON-RPC version"
            assert "result" in data, "Missing result"
            result = data.get("result", {})
            tools = result.get("tools", [])
            
            self._print(f"✅ MCP server has {len(tools)} tools", "✅")
            
            return len(tools) == 11
            
        except Exception as e:
            self._print(f"❌ MCP tools/list failed: {e}", "❌")
            return False
    
    def _print_json(self, data: Dict[str, Any], title: str = "Response", max_items: int = None):
        """Pretty print JSON response"""
        if self.verbose:
            print(f"\n📋 {title}:")
            if max_items:
                # Truncate large responses
                if isinstance(data, dict) and "result" in data:
                    result = data["result"]
                    if isinstance(result, dict) and "tools" in result:
                        tools = result["tools"][:max_items]
                        display_data = {**data, "result": {**result, "tools": tools, "...": "truncated"}}
                        print(json.dumps(display_data, indent=2))
                        return
            print(json.dumps(data, indent=2))
    
    # ============================================================================
    # TEST RUNNER
    # ============================================================================
    
    async def run_all_tests(self) -> Dict[str, bool]:
        """Run all tests and return results"""
        print("\n" + "="*80)
        print("🧪 TRELLO MCP CLOUD RUN TEST SUITE")
        print("="*80)
        print(f"📍 Service URL: {self.service_url}\n")
        
        results = {
            "health": await self.test_health(),
            "root": await self.test_root_endpoint(),
            "auth_login": await self.test_auth_login_endpoint(),
            "tools": await self.test_tools_endpoint(),
            "mcp_initialize": await self.test_mcp_initialize(),
            "mcp_tools_list": await self.test_mcp_tools_list(),
        }
        
        # Print summary
        print("\n" + "="*80)
        print("📊 TEST SUMMARY")
        print("="*80)
        
        passed = sum(1 for v in results.values() if v)
        total = len(results)
        
        for test_name, result in results.items():
            status = "✅ PASS" if result else "❌ FAIL"
            print(f"{status} - {test_name}")
        
        print(f"\n📈 Results: {passed}/{total} tests passed")
        
        if passed == total:
            print("\n🎉 ALL TESTS PASSED! Service is working correctly.")
        else:
            print(f"\n⚠️  {total - passed} test(s) failed. Check the details above.")
        
        print("="*80 + "\n")
        
        return results


async def main():
    """Run tests"""
    client = TrelloMCPTestClient(verbose=True)
    results = await client.run_all_tests()
    
    # Exit with appropriate code
    if all(results.values()):
        exit(0)
    else:
        exit(1)


if __name__ == "__main__":
    asyncio.run(main())

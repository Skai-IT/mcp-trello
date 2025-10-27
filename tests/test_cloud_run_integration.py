#!/usr/bin/env python3
"""
Unit tests for Trello MCP Cloud Run service

Run tests with:
    python -m pytest tests/test_cloud_run_integration.py -v

Or with unittest:
    python -m unittest tests.test_cloud_run_integration -v
"""

import unittest
import requests
from typing import Dict, Any

SERVICE_URL = "https://trello-mcp-116435607783.us-central1.run.app"


class TestTrelloMCPCloudRun(unittest.TestCase):
    """Unit tests for Trello MCP Cloud Run service"""

    @classmethod
    def setUpClass(cls):
        """Set up test fixtures"""
        cls.service_url = SERVICE_URL
        cls.session = requests.Session()
        cls.session.timeout = 10

    def test_01_health_endpoint(self):
        """Test health endpoint returns 200 and correct structure"""
        response = self.session.get(f"{self.service_url}/health", timeout=10)
        self.assertEqual(response.status_code, 200, "Health endpoint should return 200")

        data = response.json()
        self.assertEqual(data.get("status"), "healthy", "Status should be 'healthy'")
        self.assertEqual(data.get("tools_count"), 11, "Should have 11 tools")
        self.assertIn("mcp_server", data, "Response should contain mcp_server key")

    def test_02_root_endpoint(self):
        """Test root endpoint and feature flags"""
        response = self.session.get(f"{self.service_url}/", timeout=10)
        self.assertEqual(response.status_code, 200, "Root endpoint should return 200")

        data = response.json()
        self.assertIn("endpoints", data, "Should have endpoints")
        self.assertIn("features", data, "Should have features")

        features = data.get("features", {})
        self.assertTrue(features.get("interactive_login"), "Interactive login should be enabled")
        self.assertTrue(features.get("session_credentials_caching"), "Session caching should be enabled")

    def test_03_auth_login_endpoint(self):
        """Test interactive login endpoint"""
        response = self.session.get(f"{self.service_url}/auth/login", timeout=10)
        self.assertEqual(response.status_code, 200, "/auth/login should return 200")

        data = response.json()
        self.assertIn("login_url", data, "Should have login_url")
        self.assertIn("instructions", data, "Should have instructions")
        self.assertIn("features", data, "Should have features")

        features = data.get("features", {})
        self.assertTrue(features.get("automatic_browser_open"), "Browser auto-open should be enabled")
        self.assertTrue(features.get("session_caching"), "Session caching should be enabled")
        self.assertEqual(features.get("cache_duration_minutes"), 480, "Cache should be 8 hours (480 minutes)")

    def test_04_tools_endpoint(self):
        """Test tools endpoint has all 11 tools"""
        response = self.session.get(f"{self.service_url}/tools", timeout=10)
        self.assertEqual(response.status_code, 200, "/tools should return 200")

        data = response.json()
        tools = data.get("tools", [])
        self.assertEqual(len(tools), 11, "Should have exactly 11 tools")

        # Check tool names
        expected_tools = [
            "list_boards", "get_board", "create_board", "update_board",
            "get_lists", "create_list",
            "get_cards", "create_card", "update_card",
            "add_member_to_card", "search_cards"
        ]
        tool_names = [t.get("name") for t in tools]
        for tool_name in expected_tools:
            self.assertIn(tool_name, tool_names, f"Should have {tool_name} tool")

    def test_05_tools_optional_credentials(self):
        """Test that credentials are optional for all tools"""
        response = self.session.get(f"{self.service_url}/tools", timeout=10)
        data = response.json()
        tools = data.get("tools", [])

        for tool in tools:
            name = tool.get("name")
            schema = tool.get("inputSchema", {})
            required = schema.get("required", [])

            # api_key and token should NOT be in required list
            has_api_key = "api_key" in required
            has_token = "token" in required

            self.assertFalse(has_api_key, f"{name} should not require api_key")
            self.assertFalse(has_token, f"{name} should not require token")

    def test_06_mcp_initialize(self):
        """Test MCP initialize request"""
        mcp_request = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "initialize",
            "params": {
                "protocolVersion": "2024-11-05",
                "clientInfo": {"name": "test", "version": "1.0"}
            }
        }

        response = self.session.post(
            f"{self.service_url}/mcp",
            json=mcp_request,
            timeout=10,
            headers={"Content-Type": "application/json"}
        )
        self.assertEqual(response.status_code, 200, "MCP endpoint should return 200")

        data = response.json()
        self.assertEqual(data.get("jsonrpc"), "2.0", "Should be JSON-RPC 2.0")
        self.assertIn("result", data, "Should have result")

        result = data.get("result", {})
        self.assertIn("capabilities", result, "Result should have capabilities")

    def test_07_mcp_tools_list(self):
        """Test MCP tools/list request"""
        mcp_request = {
            "jsonrpc": "2.0",
            "id": 2,
            "method": "tools/list"
        }

        response = self.session.post(
            f"{self.service_url}/mcp",
            json=mcp_request,
            timeout=10,
            headers={"Content-Type": "application/json"}
        )
        self.assertEqual(response.status_code, 200, "MCP endpoint should return 200")

        data = response.json()
        result = data.get("result", {})
        tools = result.get("tools", [])

        self.assertEqual(len(tools), 11, "MCP should report 11 tools")


if __name__ == "__main__":
    unittest.main()

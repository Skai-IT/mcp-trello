#!/usr/bin/env python3
"""
Interactive Trello Card Creator
Helps you create a new card in your Trello board using the MCP server
"""

import asyncio
import json
import requests
import sys
from typing import Dict, Any, Optional
from datetime import datetime

# For local testing
SERVICE_URL = "http://localhost:8080"  # Local server
# For cloud testing
# SERVICE_URL = "https://trello-mcp-116435607783.us-central1.run.app"

class CardCreator:
    """Interactive card creator for Trello MCP"""
    
    def __init__(self, service_url: str = SERVICE_URL):
        self.service_url = service_url
        self.session = requests.Session()
        self.api_key = None
        self.token = None
        
    def print_section(self, title: str):
        """Print a formatted section header"""
        print(f"\n{'='*60}")
        print(f"  {title}")
        print(f"{'='*60}\n")
    
    def print_info(self, message: str):
        """Print info message"""
        print(f"ℹ️  {message}")
    
    def print_success(self, message: str):
        """Print success message"""
        print(f"✅ {message}")
    
    def print_error(self, message: str):
        """Print error message"""
        print(f"❌ {message}")
    
    def input_required(self, prompt: str, validate_func=None) -> str:
        """Get required user input"""
        while True:
            value = input(f"→ {prompt}: ").strip()
            if not value:
                print("  ⚠️  This field is required!")
                continue
            if validate_func and not validate_func(value):
                print("  ⚠️  Invalid input!")
                continue
            return value
    
    def input_optional(self, prompt: str) -> Optional[str]:
        """Get optional user input"""
        value = input(f"→ {prompt} (optional, press Enter to skip): ").strip()
        return value if value else None
    
    def call_mcp(self, tool_name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Call MCP tool"""
        payload = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "tools/call",
            "params": {
                "name": tool_name,
                "arguments": arguments
            }
        }
        
        try:
            response = self.session.post(
                f"{self.service_url}/mcp",
                json=payload,
                timeout=30
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.ConnectionError:
            self.print_error("Cannot connect to MCP server!")
            print(f"   Make sure the server is running at {self.service_url}")
            sys.exit(1)
        except Exception as e:
            self.print_error(f"Error calling MCP: {str(e)}")
            raise
    
    def get_credentials(self):
        """Get API credentials from user"""
        self.print_section("🔐 TRELLO CREDENTIALS")
        
        print("Get your credentials from: https://trello.com/app-key\n")
        
        self.api_key = self.input_required(
            "Enter your Trello API Key",
            validate_func=lambda x: len(x) >= 32
        )
        
        self.token = self.input_required(
            "Enter your Trello Token",
            validate_func=lambda x: len(x) >= 32
        )
        
        self.print_success("Credentials received!")
    
    def list_boards(self) -> Dict[str, Any]:
        """List user's boards"""
        self.print_info("Fetching your boards...")
        
        result = self.call_mcp("list_boards", {
            "api_key": self.api_key,
            "token": self.token
        })
        
        return result
    
    def get_lists(self, board_id: str) -> Dict[str, Any]:
        """Get lists from a board"""
        self.print_info(f"Fetching lists from board {board_id}...")
        
        result = self.call_mcp("get_lists", {
            "api_key": self.api_key,
            "token": self.token,
            "board_id": board_id
        })
        
        return result
    
    def select_board(self) -> tuple:
        """Let user select a board"""
        self.print_section("📋 SELECT BOARD")
        
        # Get boards
        result = self.list_boards()
        
        if "error" in result:
            self.print_error(f"Error getting boards: {result['error']}")
            sys.exit(1)
        
        # Parse boards from result
        boards = result.get("result", {}).get("boards", [])
        
        if not boards:
            self.print_error("No boards found!")
            sys.exit(1)
        
        # Show boards
        print("Your boards:\n")
        for i, board in enumerate(boards, 1):
            board_name = board.get("name", "Unknown")
            board_id = board.get("id", "unknown")
            print(f"  {i}. {board_name} (ID: {board_id})")
        
        # Get selection
        print()
        while True:
            try:
                choice = int(input("→ Select board number: "))
                if 1 <= choice <= len(boards):
                    selected_board = boards[choice - 1]
                    self.print_success(f"Selected: {selected_board['name']}")
                    return selected_board["id"], selected_board["name"]
                else:
                    print("  ⚠️  Invalid selection!")
            except ValueError:
                print("  ⚠️  Please enter a number!")
    
    def select_list(self, board_id: str, board_name: str) -> tuple:
        """Let user select a list"""
        self.print_section("📝 SELECT LIST")
        
        print(f"Board: {board_name}\n")
        
        # Get lists
        result = self.get_lists(board_id)
        
        if "error" in result:
            self.print_error(f"Error getting lists: {result['error']}")
            sys.exit(1)
        
        # Parse lists from result
        lists = result.get("result", {}).get("lists", [])
        
        if not lists:
            self.print_error("No lists found!")
            sys.exit(1)
        
        # Show lists
        print("Lists:\n")
        for i, lst in enumerate(lists, 1):
            list_name = lst.get("name", "Unknown")
            list_id = lst.get("id", "unknown")
            print(f"  {i}. {list_name} (ID: {list_id})")
        
        # Get selection
        print()
        while True:
            try:
                choice = int(input("→ Select list number: "))
                if 1 <= choice <= len(lists):
                    selected_list = lists[choice - 1]
                    self.print_success(f"Selected: {selected_list['name']}")
                    return selected_list["id"], selected_list["name"]
                else:
                    print("  ⚠️  Invalid selection!")
            except ValueError:
                print("  ⚠️  Please enter a number!")
    
    def get_card_details(self) -> Dict[str, Any]:
        """Get card details from user"""
        self.print_section("🎫 CARD DETAILS")
        
        card = {}
        
        # Card name (required)
        card["name"] = self.input_required("Card title/name")
        
        # Description (optional)
        card["desc"] = self.input_optional("Card description")
        
        # Due date (optional)
        due = self.input_optional("Due date (YYYY-MM-DD format)")
        if due:
            try:
                # Validate date format
                datetime.strptime(due, "%Y-%m-%d")
                card["due"] = due + "T23:59:59Z"
            except ValueError:
                print("  ⚠️  Invalid date format, skipping due date")
        
        # Labels (optional)
        labels_str = self.input_optional("Labels (comma-separated)")
        if labels_str:
            card["labels"] = [l.strip() for l in labels_str.split(",")]
        
        return card
    
    def create_card(self, list_id: str, card_details: Dict[str, Any]) -> Dict[str, Any]:
        """Create the card"""
        self.print_info("Creating card...")
        
        # Add list_id and credentials to arguments
        arguments = {
            "api_key": self.api_key,
            "token": self.token,
            "list_id": list_id,
            **card_details
        }
        
        result = self.call_mcp("create_card", arguments)
        
        return result
    
    def display_result(self, result: Dict[str, Any]):
        """Display the result"""
        self.print_section("✨ RESULT")
        
        if "error" in result:
            self.print_error(f"Card creation failed: {result['error']}")
            if "message" in result:
                print(f"   Details: {result['message']}")
        else:
            card_data = result.get("result", {})
            if card_data:
                self.print_success("Card created successfully!")
                print(f"\nCard Details:")
                print(f"  • ID: {card_data.get('id', 'N/A')}")
                print(f"  • Name: {card_data.get('name', 'N/A')}")
                print(f"  • Board: {card_data.get('board_id', 'N/A')}")
                print(f"  • List: {card_data.get('list_id', 'N/A')}")
                if card_data.get('desc'):
                    print(f"  • Description: {card_data['desc']}")
                if card_data.get('due'):
                    print(f"  • Due: {card_data['due']}")
                if card_data.get('url'):
                    print(f"  • URL: {card_data['url']}")
                print()
                return True
        
        return False
    
    def run(self):
        """Run the interactive card creator"""
        print("\n" + "="*60)
        print("  🎯 TRELLO MCP - INTERACTIVE CARD CREATOR")
        print("="*60)
        
        try:
            # Step 1: Get credentials
            self.get_credentials()
            
            # Step 2: Select board
            board_id, board_name = self.select_board()
            
            # Step 3: Select list
            list_id, list_name = self.select_list(board_id, board_name)
            
            # Step 4: Get card details
            card_details = self.get_card_details()
            
            # Step 5: Create card
            result = self.create_card(list_id, card_details)
            
            # Step 6: Display result
            self.display_result(result)
            
            # Success message
            print("\n" + "="*60)
            print("  ✅ CARD CREATION COMPLETE")
            print("  Check your Trello board to see the new card!")
            print("="*60 + "\n")
            
        except KeyboardInterrupt:
            print("\n\n❌ Card creation cancelled by user")
            sys.exit(0)
        except Exception as e:
            print(f"\n❌ Error: {str(e)}")
            sys.exit(1)


if __name__ == "__main__":
    creator = CardCreator()
    creator.run()

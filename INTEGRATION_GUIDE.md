# 🔗 Trello MCP Integration Guide

Complete instructions for integrating Trello MCP with Claude Desktop, VS Code, Cursor, and other tools.

**Last Updated:** October 27, 2025  
**Service URL:** https://trello-mcp-116435607783.us-central1.run.app

---

## 📋 Table of Contents

1. [Quick Links](#quick-links)
2. [Claude Desktop](#-claude-desktop)
3. [VS Code](#-vs-code)
4. [Cursor](#-cursor)
5. [Cline (VS Code Extension)](#-cline-vs-code-extension)
6. [Other Tools](#-other-tools)
7. [Custom Integration](#-custom-integration)
8. [Troubleshooting](#-troubleshooting)

---

## Quick Links

| Tool | Config File | Time | Link |
|------|-------------|------|------|
| **Claude Desktop** | `claude_desktop_config.json` | 5 min | [👇 Setup](#-claude-desktop) |
| **VS Code** | `settings.json` | 3 min | [👇 Setup](#-vs-code) |
| **Cursor** | `settings.json` | 3 min | [👇 Setup](#-cursor) |
| **Cline** | `settings.json` | 3 min | [👇 Setup](#-cline-vs-code-extension) |
| **LM Studio** | `mcp-servers.json` | 5 min | [👇 Setup](#-lm-studio) |
| **Zed** | `settings.json` | 3 min | [👇 Setup](#-zed) |
| **Custom** | Code | Varies | [👇 Setup](#-custom-integration) |

---

## 🤖 Claude Desktop

### Prerequisites
- ✅ Python 3.7+
- ✅ Claude Desktop installed
- ✅ Internet connection

### Step-by-Step Setup

#### 1. Download Proxy Server
```bash
curl -o ~/trello_mcp_server.py https://raw.githubusercontent.com/Skai-IT/mcp-trello/main/trello_mcp_server.py
chmod +x ~/trello_mcp_server.py
```

#### 2. Install Dependencies
```bash
pip3 install httpx
```

Verify installation:
```bash
python3 -c "import httpx; print('✅ httpx installed')"
```

#### 3. Configure Claude Desktop

**On macOS:**
```bash
# Create config directory if needed
mkdir -p ~/Library/Application\ Support/Claude

# Open config file
nano ~/Library/Application\ Support/Claude/claude_desktop_config.json
```

**Windows:**
```bash
%APPDATA%\Claude\claude_desktop_config.json
```

**Add this configuration:**
```json
{
  "mcpServers": {
    "trello-mcp": {
      "command": "python3",
      "args": ["/Users/YOUR_USERNAME/trello_mcp_server.py"],
      "env": {
        "TRELLO_MCP_URL": "https://trello-mcp-116435607783.us-central1.run.app",
        "TRELLO_MCP_TYPE": "cloud_run"
      }
    }
  }
}
```

⚠️ **Replace `/Users/YOUR_USERNAME/`** with your actual home directory.

**Find your home directory:**
```bash
echo $HOME
# Output: /Users/shlomisha
# Use: /Users/shlomisha/trello_mcp_server.py
```

#### 4. Restart Claude Desktop
- **Close** Claude completely (quit from dock/system tray)
- **Wait** 2 seconds
- **Reopen** Claude
- Trello MCP should now be connected

#### 5. Verify Connection

In Claude, try these prompts:
```
List my Trello boards

Show me all cards in my boards

Create a board called "Test Board"

Search for urgent cards
```

Claude will now use your Trello MCP to interact with Trello.

### Testing

Create a simple test:
```
Can you create a card called "Test Card" on my first board?
```

Claude should:
1. Connect to your Trello account (browser may open)
2. Authenticate (paste API key and token if prompted)
3. List your boards
4. Create a card on the first board
5. Confirm completion

---

## 📝 VS Code

### Prerequisites
- ✅ VS Code installed
- ✅ Python 3.7+
- ✅ Basic knowledge of VS Code settings

### Step-by-Step Setup

#### 1. Download Proxy Server
```bash
curl -o ~/trello_mcp_server.py https://raw.githubusercontent.com/Skai-IT/mcp-trello/main/trello_mcp_server.py
chmod +x ~/trello_mcp_server.py
```

#### 2. Install Dependencies
```bash
pip3 install httpx
```

#### 3. Configure VS Code

**Open settings.json:**
- Press `Cmd + ,` (Mac) or `Ctrl + ,` (Windows/Linux)
- Search for "settings"
- Click the "Open Settings (JSON)" icon in top right
- Or manually edit: `~/.vscode/settings.json`

**Add this configuration:**
```json
{
  "mcp": {
    "mcpServers": {
      "trello-mcp": {
        "command": "python3",
        "args": ["/Users/YOUR_USERNAME/trello_mcp_server.py"],
        "env": {
          "TRELLO_MCP_URL": "https://trello-mcp-116435607783.us-central1.run.app",
          "TRELLO_MCP_TYPE": "cloud_run"
        }
      }
    }
  }
}
```

#### 4. Restart VS Code
- Close VS Code completely
- Reopen it
- Wait for initialization (5-10 seconds)

#### 5. Verify Connection

**Open Developer Console:**
- Mac: `Cmd + Shift + J`
- Windows/Linux: `Ctrl + Shift + J`

**Look for:**
```
MCP Server connected: trello-mcp
✅ No errors = Success
```

---

## 🖥️ Cursor

### Prerequisites
- ✅ Cursor installed
- ✅ Python 3.7+
- ✅ httpx installed

### Setup

#### 1-2: Download & Install (Same as VS Code)
```bash
curl -o ~/trello_mcp_server.py https://raw.githubusercontent.com/Skai-IT/mcp-trello/main/trello_mcp_server.py
chmod +x ~/trello_mcp_server.py
pip3 install httpx
```

#### 3. Configure Cursor

**File location depends on OS:**

**macOS:**
```bash
~/.cursor/settings.json
# or
~/.config/Cursor/User/settings.json
```

**Windows:**
```
%APPDATA%\Cursor\User\settings.json
```

**Add configuration:**
```json
{
  "mcp": {
    "mcpServers": {
      "trello-mcp": {
        "command": "python3",
        "args": ["/Users/YOUR_USERNAME/trello_mcp_server.py"],
        "env": {
          "TRELLO_MCP_URL": "https://trello-mcp-116435607783.us-central1.run.app"
        }
      }
    }
  }
}
```

#### 4. Restart Cursor
- Close Cursor
- Reopen it
- Trello tools are now available

---

## 🤖 Cline (VS Code Extension)

Cline is an autonomous AI agent for VS Code that works with MCP tools.

### Prerequisites
- ✅ VS Code with Cline extension installed
- ✅ Python 3.7+
- ✅ Proxy server downloaded

### Setup

#### 1. Download & Install
```bash
curl -o ~/trello_mcp_server.py https://raw.githubusercontent.com/Skai-IT/mcp-trello/main/trello_mcp_server.py
chmod +x ~/trello_mcp_server.py
pip3 install httpx
```

#### 2. Configure VS Code (Same as above)
Add to `~/.vscode/settings.json`:
```json
{
  "mcp": {
    "mcpServers": {
      "trello-mcp": {
        "command": "python3",
        "args": ["/Users/YOUR_USERNAME/trello_mcp_server.py"],
        "env": {
          "TRELLO_MCP_URL": "https://trello-mcp-116435607783.us-central1.run.app"
        }
      }
    }
  }
}
```

#### 3. Restart VS Code
- Close and reopen VS Code

#### 4. Use with Cline

In Cline chat, you can now:
```
Create a Trello board for the Q4 roadmap

Move all urgent cards to the top list

Generate a status report of all cards

Organize cards by priority
```

Cline will intelligently use the Trello MCP tools to complete tasks.

---

## 🛠️ Other Tools

### LM Studio

LM Studio is a local LLM interface with MCP support.

**Configuration file:** `~/.lm-studio/mcp-servers.json`

```json
{
  "servers": [
    {
      "name": "trello-mcp",
      "type": "stdio",
      "command": "python3",
      "args": ["/Users/YOUR_USERNAME/trello_mcp_server.py"],
      "env": {
        "TRELLO_MCP_URL": "https://trello-mcp-116435607783.us-central1.run.app"
      }
    }
  ]
}
```

### Zed

Zed is a high-performance code editor.

**Configuration file:** `~/.config/zed/settings.json`

```json
{
  "mcp_servers": {
    "trello-mcp": {
      "command": "python3",
      "args": ["/Users/YOUR_USERNAME/trello_mcp_server.py"],
      "env": {
        "TRELLO_MCP_URL": "https://trello-mcp-116435607783.us-central1.run.app"
      }
    }
  }
}
```

### Other IDEs/Editors

If your editor supports MCP, use this template:

```json
{
  "mcp": {
    "mcpServers": {
      "trello-mcp": {
        "command": "python3",
        "args": ["/path/to/trello_mcp_server.py"],
        "env": {
          "TRELLO_MCP_URL": "https://trello-mcp-116435607783.us-central1.run.app"
        }
      }
    }
  }
}
```

---

## 🔧 Custom Integration

### Python Client

```python
#!/usr/bin/env python3
"""
Trello MCP Client - Python example
"""

import httpx
import json
from typing import Dict, Any, Optional

class TrelloMCPClient:
    def __init__(self, service_url: str):
        """Initialize client with service URL"""
        self.service_url = service_url
        self.client = httpx.Client(timeout=30.0)
    
    def call_tool(self, tool_name: str, **params) -> Dict[str, Any]:
        """Call a Trello MCP tool"""
        request = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": tool_name,
            "params": params
        }
        
        response = self.client.post(
            f"{self.service_url}/mcp",
            json=request
        )
        return response.json()
    
    def list_boards(self) -> Dict[str, Any]:
        """List all Trello boards"""
        return self.call_tool("list_boards")
    
    def get_board(self, board_id: str) -> Dict[str, Any]:
        """Get board details"""
        return self.call_tool("get_board", board_id=board_id)
    
    def create_board(self, name: str, desc: str = "") -> Dict[str, Any]:
        """Create a new board"""
        return self.call_tool("create_board", name=name, desc=desc)
    
    def get_cards(self, board_id: str, list_id: Optional[str] = None) -> Dict[str, Any]:
        """Get cards from board or list"""
        params = {"board_id": board_id}
        if list_id:
            params["list_id"] = list_id
        return self.call_tool("get_cards", **params)
    
    def create_card(self, board_id: str, list_id: str, name: str, 
                   desc: str = "") -> Dict[str, Any]:
        """Create a new card"""
        return self.call_tool("create_card", 
                            board_id=board_id, 
                            list_id=list_id, 
                            name=name, 
                            desc=desc)
    
    def search_cards(self, query: str, board_id: Optional[str] = None) -> Dict[str, Any]:
        """Search for cards"""
        params = {"query": query}
        if board_id:
            params["board_id"] = board_id
        return self.call_tool("search_cards", **params)
    
    def close(self):
        """Close client connection"""
        self.client.close()


# Example Usage
if __name__ == "__main__":
    client = TrelloMCPClient(
        "https://trello-mcp-116435607783.us-central1.run.app"
    )
    
    try:
        # List boards
        print("📋 Listing boards...")
        boards = client.list_boards()
        print(json.dumps(boards, indent=2))
        
        # Create a board
        print("\n✨ Creating board...")
        new_board = client.create_board(
            "My Project",
            "Project description"
        )
        print(json.dumps(new_board, indent=2))
        
    finally:
        client.close()
```

### JavaScript/Node.js Client

```javascript
/**
 * Trello MCP Client - JavaScript example
 */

class TrelloMCPClient {
  constructor(serviceUrl) {
    this.serviceUrl = serviceUrl;
  }

  async callTool(toolName, params = {}) {
    const request = {
      jsonrpc: '2.0',
      id: 1,
      method: toolName,
      params: params
    };

    const response = await fetch(`${this.serviceUrl}/mcp`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(request)
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    return response.json();
  }

  async listBoards() {
    return this.callTool('list_boards', {});
  }

  async getBoard(boardId) {
    return this.callTool('get_board', { board_id: boardId });
  }

  async createBoard(name, desc = '') {
    return this.callTool('create_board', { name, desc });
  }

  async getCards(boardId, listId = null) {
    const params = { board_id: boardId };
    if (listId) params.list_id = listId;
    return this.callTool('get_cards', params);
  }

  async createCard(boardId, listId, name, desc = '') {
    return this.callTool('create_card', {
      board_id: boardId,
      list_id: listId,
      name,
      desc
    });
  }

  async searchCards(query, boardId = null) {
    const params = { query };
    if (boardId) params.board_id = boardId;
    return this.callTool('search_cards', params);
  }
}

// Example Usage
(async () => {
  const client = new TrelloMCPClient(
    'https://trello-mcp-116435607783.us-central1.run.app'
  );

  try {
    // List boards
    console.log('📋 Listing boards...');
    const boards = await client.listBoards();
    console.log(JSON.stringify(boards, null, 2));

    // Create board
    console.log('\n✨ Creating board...');
    const newBoard = await client.createBoard(
      'My Project',
      'Project description'
    );
    console.log(JSON.stringify(newBoard, null, 2));

  } catch (error) {
    console.error('Error:', error);
  }
})();
```

### cURL Examples

```bash
# List boards
curl -X POST https://trello-mcp-116435607783.us-central1.run.app/mcp \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "id": 1,
    "method": "list_boards",
    "params": {}
  }'

# Create a board
curl -X POST https://trello-mcp-116435607783.us-central1.run.app/mcp \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "id": 1,
    "method": "create_board",
    "params": {
      "name": "My Project",
      "desc": "Project description"
    }
  }'

# Search for cards
curl -X POST https://trello-mcp-116435607783.us-central1.run.app/mcp \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "id": 1,
    "method": "search_cards",
    "params": {
      "query": "urgent"
    }
  }'
```

---

## 🆘 Troubleshooting

### General Issues

#### "httpx not found"
```bash
# Install httpx
pip3 install httpx

# Verify
python3 -c "import httpx; print('✅ OK')"
```

#### "Permission denied: trello_mcp_server.py"
```bash
# Make executable
chmod +x ~/trello_mcp_server.py
```

#### "Command not found: python3"
```bash
# Check Python version
python --version

# Try python instead of python3
# Or install Python 3: https://www.python.org/downloads/
```

### Connection Issues

#### "MCP Server not connecting"

**Checklist:**
1. ✅ Proxy server is running: `python3 ~/trello_mcp_server.py` (Ctrl+C to stop)
2. ✅ Config file syntax valid: `python3 -m json.tool ~/.vscode/settings.json`
3. ✅ Path is correct: `echo $HOME`
4. ✅ Application restarted: Close completely and reopen
5. ✅ Service is up: `curl https://trello-mcp-116435607783.us-central1.run.app/health`

#### "Connection timeout"
```bash
# Test service
curl https://trello-mcp-116435607783.us-central1.run.app/health

# If fails: Check internet, verify URL
```

#### "Service unreachable"
```bash
# Check Cloud Run service
gcloud run services list --region=us-central1

# Check logs
gcloud run logs read trello-mcp --region=us-central1 --limit=50
```

### Authentication Issues

#### "First request hangs / browser doesn't open"
- Proxy server needs browser access
- Make sure you have a GUI (not SSH-only)
- Try again, browser should open
- If not, manually visit: `https://trello.com/app-key`

#### "Credentials error: Invalid API key"
- Check API key format (32 characters)
- Visit: https://trello.com/app-key
- Generate new token if needed
- Try again

#### "Session expired"
- Credentials cached for 8 hours
- After 8 hours, first request will prompt again
- This is normal

### Configuration Issues

#### "JSON syntax error"
```bash
# Validate JSON
python3 -m json.tool ~/.vscode/settings.json

# If fails, check for:
# - Missing commas
# - Mismatched quotes
# - Trailing commas
```

#### "Path not found"
```bash
# Check file exists
ls -la ~/trello_mcp_server.py

# Check path is correct
echo $HOME
# Compare with path in config
```

### Getting Help

**Resources:**
- Check logs: Application developer console or terminal
- Read config file: Ensure it matches examples
- Test service: `curl` commands in Troubleshooting section
- GitHub issues: https://github.com/Skai-IT/mcp-trello/issues

---

## 📞 Support

**Service Status:** https://trello-mcp-116435607783.us-central1.run.app/health

**Documentation:**
- Main README: See main project README.md
- Quick Start: QUICKSTART.md
- Architecture: DEPLOYMENT_SUMMARY.md

---

**Happy integrating! 🚀**

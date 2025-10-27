# 📋 Trello MCP Server

A production-ready **Model Context Protocol (MCP) server** for seamless Trello integration with AI agents and Claude Desktop. Deploy to Google Cloud Run in minutes!

## 🎯 What This Is

This MCP server provides **11 comprehensive Trello tools** that allow AI agents to:
- Manage boards, lists, and cards
- Create and update content
- Search and organize projects
- Assign team members
- Track progress and deadlines

**Perfect for:** Project management automation, AI-driven task organization, and intelligent Trello workflows.

## ✨ Key Features

### 🔐 **Interactive Login System** (NEW!)
- **Browser-based authentication** - Automatic pop-up to Trello login page
- **Session credential caching** - 8-hour auto-cache, no disk storage
- **Optional credentials** - First request prompts, subsequent requests use cache
- **Secure by default** - Never asks for credentials more than once per session
- See: `QUICK_START_LOGIN.txt` | `INTERACTIVE_LOGIN_GUIDE.md`

### 🔒 **Security First**
- **Per-request credentials** - API keys never stored
- **Input validation** with Pydantic schemas
- **Multi-tenant safe** - isolated by user credentials
- **Rate limiting** - respects Trello's API limits (300 req/10s)

### 🚀 **Production Ready**  
- **Google Cloud Run optimized** - fast startup, graceful shutdown
- **Health checks** - `/health` endpoint for monitoring
- **Structured logging** - JSON format for Cloud Logging
- **Error handling** - comprehensive error messages
- **Docker containerized** - multi-stage build <200MB

### 🛠️ **Complete Toolset**
- **Board Management**: List, get, create, update boards
- **List Management**: Get lists, create new lists
- **Card Management**: Get, create, update cards, assign members, search

## 📦 What's Included

```
trello_mcp_server/
├── main.py              # HTTP server (156 lines)
├── mcp_server.py        # MCP protocol handler (148 lines)  
├── trello_client.py     # Trello API wrapper (340 lines)
├── tools.py             # 11 Trello tools (522 lines)
├── schemas.py           # Pydantic models (40 lines)
├── config.py            # Configuration (22 lines)
├── logging_config.py    # Structured logging (47 lines)
├── Dockerfile           # Multi-stage container
├── cloudbuild.yaml      # CI/CD pipeline
├── requirements.txt     # Dependencies
├── .dockerignore        # Build optimization
├── START_HERE.txt       # Quick orientation
├── QUICKSTART.md        # 5-minute deployment
└── README.md            # This file
```

**Total**: ~1,300 lines of production code

## 🚀 Quick Start

### 1. Get Trello Credentials
```bash
# Go to: https://trello.com/app-key
# Copy: API Key + Token
```

### 2. Deploy to Cloud Run  
```bash
cd trello_mcp_server
export PROJECT_ID="your-gcp-project"

# Enable APIs
gcloud services enable run.googleapis.com cloudbuild.googleapis.com

# Build & Deploy
gcloud builds submit --tag gcr.io/$PROJECT_ID/trello-mcp:latest .
gcloud run deploy trello-mcp \
  --image gcr.io/$PROJECT_ID/trello-mcp:latest \
  --region us-central1 \
  --allow-unauthenticated \
  --memory 512Mi
```

### 3. Test Your Server
```bash
curl https://your-service-url/health
# Expected: {"status":"healthy","service":"trello-mcp",...}
```

**Full deployment guide**: See `QUICKSTART.md`

## 🛠️ All 11 Tools

| Category | Tool | Description |
|----------|------|-------------|
| **Boards** | `list_boards` | List all user boards |
| | `get_board` | Get detailed board information |
| | `create_board` | Create a new board |
| | `update_board` | Update board settings |
| **Lists** | `get_lists` | Get all lists on a board |
| | `create_list` | Create a new list |
| **Cards** | `get_cards` | Get cards from board or list |
| | `create_card` | Create a new card |
| | `update_card` | Update existing card |
| | `add_member_to_card` | Assign member to card |
| | `search_cards` | Search cards across boards |

## 📋 Usage Examples

### MCP Protocol Integration

All tools follow the JSON-RPC 2.0 MCP protocol:

```json
POST /mcp
{
  "jsonrpc": "2.0",
  "method": "tools/call",
  "id": 1,
  "params": {
    "name": "list_boards", 
    "arguments": {
      "api_key": "your-trello-api-key",
      "token": "your-trello-token"
    }
  }
}
```

### Create a New Board
```json
{
  "jsonrpc": "2.0",
  "method": "tools/call",
  "id": 2,
  "params": {
    "name": "create_board",
    "arguments": {
      "api_key": "your-api-key",
      "token": "your-token", 
      "name": "Q4 Project Planning",
      "desc": "Planning board for Q4 initiatives",
      "prefs": {
        "permissionLevel": "org",
        "background": "blue"
      }
    }
  }
}
```

### Search for Urgent Cards
```json
{
  "jsonrpc": "2.0",
  "method": "tools/call",
  "id": 3,
  "params": {
    "name": "search_cards",
    "arguments": {
      "api_key": "your-api-key",
      "token": "your-token",
      "query": "urgent OR priority:high",
      "limit": 50
    }
  }
}
```

### Create and Assign a Card
```json
{
  "jsonrpc": "2.0",
  "method": "tools/call", 
  "id": 4,
  "params": {
    "name": "create_card",
    "arguments": {
      "api_key": "your-api-key",
      "token": "your-token",
      "name": "Implement new feature",
      "list_id": "list-id-here",
      "desc": "Detailed description of the feature requirements",
      "due": "2024-12-31T23:59:59Z",
      "members": ["member-id-1", "member-id-2"]
    }
  }
}
```

## 🔗 Integration Guide

### ⭐ Claude Desktop Integration

#### Step 1: Download the Proxy Server
```bash
# Get the proxy server that connects to Cloud Run
curl -o ~/trello_mcp_server.py https://raw.githubusercontent.com/Skai-IT/mcp-trello/main/trello_mcp_server.py
chmod +x ~/trello_mcp_server.py
```

#### Step 2: Install Dependencies
```bash
pip3 install httpx
```

#### Step 3: Configure Claude Desktop
**File location:** `~/Library/Application Support/Claude/claude_desktop_config.json`

Add this configuration:
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

**⚠️ Important:** Replace `YOUR_USERNAME` with your home directory (run `echo $HOME`)

#### Step 4: Restart Claude Desktop
- Close Claude completely
- Reopen it
- The Trello MCP should now be available

#### Step 5: Verify Connection
In Claude, try:
```
List my Trello boards
```

Claude will connect to your Trello account and show your boards.

---

### VS Code Integration

#### Configuration File
**File location:** `~/.vscode/settings.json`

Add this to your settings:
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

Replace `YOUR_USERNAME` with your home directory.

#### Verify Connection
1. Restart VS Code
2. Open Developer Console: `Cmd + Shift + J` (Mac)
3. Look for: "MCP Server connected"
4. No errors = ✅ Success!

---

### Cursor Integration

#### Step 1: Get Proxy Server
Same as Claude Desktop - download `trello_mcp_server.py`

#### Step 2: Install Dependencies
```bash
pip3 install httpx
```

#### Step 3: Configure Cursor
**File location:** `~/.cursor/settings.json` or `~/.config/Cursor/User/settings.json`

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

#### Step 4: Restart Cursor
- Close Cursor completely
- Reopen it
- Trello MCP is ready to use

---

### Cline (VS Code Extension) Integration

Cline is an autonomous AI agent for VS Code.

#### Configuration
Add to your VS Code `settings.json`:
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

#### Using with Cline
1. Open Cline in VS Code
2. Start a new task
3. Ask Cline: "Use the Trello MCP to create a board called 'Q4 Planning'"
4. Cline will use the MCP tools to interact with Trello

---

### LM Studio Integration

LM Studio is a local LLM interface that supports MCP.

#### Configuration
**File location:** `~/.lm-studio/mcp-servers.json`

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

---

### Zed Integration

Zed is a high-performance code editor with MCP support.

#### Configuration
**File location:** `~/.config/zed/settings.json`

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

---

### Custom AI Integration

#### Python Client Example
```python
import httpx
import json

class TrelloMCPClient:
    def __init__(self, service_url):
        self.service_url = service_url
        self.client = httpx.Client()
    
    def call_tool(self, tool_name, **params):
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
    
    def list_boards(self):
        """List all Trello boards"""
        return self.call_tool("list_boards", {})
    
    def create_card(self, board_id, list_id, name, description=""):
        """Create a new Trello card"""
        return self.call_tool("create_card", {
            "board_id": board_id,
            "list_id": list_id,
            "name": name,
            "description": description
        })

# Usage
client = TrelloMCPClient("https://trello-mcp-116435607783.us-central1.run.app")
boards = client.list_boards()
print(boards)
```

#### JavaScript/Node.js Client Example
```javascript
const fetch = require('node-fetch');

class TrelloMCPClient {
  constructor(serviceUrl) {
    this.serviceUrl = serviceUrl;
  }

  async callTool(toolName, params) {
    const request = {
      jsonrpc: '2.0',
      id: 1,
      method: toolName,
      params: params
    };

    const response = await fetch(`${this.serviceUrl}/mcp`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(request)
    });

    return response.json();
  }

  async listBoards() {
    return this.callTool('list_boards', {});
  }

  async createCard(boardId, listId, name, description = '') {
    return this.callTool('create_card', {
      board_id: boardId,
      list_id: listId,
      name: name,
      description: description
    });
  }
}

// Usage
const client = new TrelloMCPClient('https://trello-mcp-116435607783.us-central1.run.app');
client.listBoards().then(boards => console.log(boards));
```

---

### Integration Summary Table

| Tool | Type | Config File | Status |
|------|------|-------------|--------|
| **Claude Desktop** | 🤖 AI Agent | `claude_desktop_config.json` | ✅ Fully Supported |
| **VS Code** | 📝 Editor | `.vscode/settings.json` | ✅ Fully Supported |
| **Cursor** | 📝 Editor | `.cursor/settings.json` | ✅ Fully Supported |
| **Cline** | 🤖 VS Code Extension | `.vscode/settings.json` | ✅ Fully Supported |
| **LM Studio** | 🤖 Local LLM | `.lm-studio/mcp-servers.json` | ✅ Supported |
| **Zed** | 📝 Editor | `.config/zed/settings.json` | ✅ Supported |
| **Custom Python** | 🔧 Client | N/A | ✅ Examples Provided |
| **Custom Node.js** | 🔧 Client | N/A | ✅ Examples Provided |

---

### Getting Started with Each Tool

#### For Claude Desktop
1. ✅ Download proxy server
2. ✅ Install httpx
3. ✅ Add config to `claude_desktop_config.json`
4. ✅ Restart Claude
5. 🎯 Start using Trello tools!

#### For VS Code / Cursor
1. ✅ Download proxy server
2. ✅ Install httpx
3. ✅ Add config to settings.json
4. ✅ Restart editor
5. 🎯 Open MCP tools in your editor!

#### For Custom Integration
1. ✅ Get service URL
2. ✅ Use provided client code
3. ✅ Call tools via JSON-RPC
4. 🎯 Integrate into your application!

---

### Troubleshooting Integration

**Problem: "MCP Server not connecting"**
- Verify proxy server is running: `python3 ~/trello_mcp_server.py`
- Check config file syntax (validate JSON)
- Ensure path is correct: `echo $HOME`
- Restart the application

**Problem: "Credentials error"**
- First tool call will prompt for auth
- Browser should auto-open to Trello
- Copy API key and token when prompted
- Credentials cached for 8 hours

**Problem: "Connection timeout"**
- Check internet connectivity
- Verify Cloud Run service is running
- Test: `curl https://trello-mcp-116435607783.us-central1.run.app/health`

**Problem: "httpx not found"**
- Install: `pip3 install httpx`
- Verify: `python3 -c "import httpx"`

### Custom AI Agent Integration

See the **Integration Guide** section above for:
- Python client example for custom AI agents
- JavaScript/Node.js client example
- Full implementation patterns

## 🏗️ Architecture

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   AI Agent      │────│  Trello MCP      │────│   Trello API    │
│   (Claude)      │    │  Server          │    │                 │
└─────────────────┘    └──────────────────┘    └─────────────────┘
        │                        │                        │
        │ MCP Protocol           │ HTTP/REST              │
        │ (JSON-RPC 2.0)         │                        │
        └────────────────────────┴────────────────────────┘
                              
Components:
• FastAPI HTTP Server (main.py)
• MCP Protocol Handler (mcp_server.py) 
• Trello API Client (trello_client.py)
• 11 Tools Implementation (tools.py)
• Security & Validation (schemas.py)
```

## 🔐 Security Model

### Credential Handling
- **Never stored**: API keys requested per-call
- **Validation**: Credentials validated on each request
- **Isolation**: Each request isolated by user credentials
- **No persistence**: Stateless server design

### Input Validation
```python
# All inputs validated with Pydantic
class CreateCardRequest(BaseModel):
    name: str = Field(..., max_length=16384)
    list_id: str = Field(..., min_length=1)
    desc: Optional[str] = Field(None, max_length=16384)
    
    @validator('name')
    def validate_name(cls, v):
        if not v.strip():
            raise ValueError("Card name cannot be empty")
        return v.strip()
```

### Rate Limiting
```python
# Respects Trello's 300 requests per 10 seconds
class RateLimiter:
    def __init__(self, max_requests=300, time_window=10):
        # Implementation ensures compliance
```

## 📊 Monitoring & Observability

### Health Checks
```bash
GET /health
{
  "status": "healthy",
  "service": "trello-mcp", 
  "version": "1.0.0",
  "timestamp": "2024-01-01T00:00:00Z",
  "mcp_server": "initialized",
  "tools_count": 11
}
```

### Structured Logging
```json
{
  "timestamp": "2024-01-01T00:00:00Z",
  "severity": "INFO",
  "message": "Tool execution completed: create_card",
  "logger": "trello_mcp",
  "service": "trello-mcp",
  "version": "v1.0.0"
}
```

### Error Handling
```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "error": {
    "code": -32603,
    "message": "Unauthorized - check your API key and token",
    "data": "Invalid API credentials provided"
  }
}
```

## 💰 Cost Breakdown

**Monthly costs on Google Cloud Run:**

| Component | Cost |
|-----------|------|
| Cloud Run (2M free requests) | **FREE** |
| Container Registry | ~$0.40 |
| Cloud Logging | ~$1.00 |
| **Total** | **~$1-2** |

**Cost factors:**
- Free tier: 2 million requests/month
- $0.40 per million requests after free tier
- Minimal storage and logging costs

## 🚀 Advanced Configuration

### Environment Variables
```bash
# Server configuration
DEBUG=false
LOG_LEVEL=INFO
REQUEST_TIMEOUT=30
MAX_RETRIES=3

# NEW: Optional pre-configured credentials (for non-interactive deployment)
# When set, these will be automatically loaded at startup
# Set BOTH for non-interactive mode, or neither for interactive login
TRELLO_USERNAME=your-api-key        # Trello API key
TRELLO_PASSWORD=your-api-token      # Trello API token

# Cloud Run auto-injected
K_SERVICE=trello-mcp
K_REVISION=trello-mcp-00001-abc
PORT=8080
```

**For detailed environment variable documentation**, see [ENV_VARIABLES.md](./ENV_VARIABLES.md)

**Using Pre-configured Credentials (Cloud Run):**
```bash
gcloud run deploy trello-mcp \
  --source . \
  --region us-central1 \
  --set-env-vars="TRELLO_USERNAME=your-api-key,TRELLO_PASSWORD=your-api-token" \
  --allow-unauthenticated
```

**Using Cloud Secrets (Recommended):**
```bash
# Create secrets
gcloud secrets create trello-api-key --replication-policy="automatic" --data-file=- <<< "your-api-key"
gcloud secrets create trello-api-token --replication-policy="automatic" --data-file=- <<< "your-api-token"

# Deploy with secrets
gcloud run deploy trello-mcp \
  --source . \
  --region us-central1 \
  --set-env-vars="TRELLO_USERNAME=projects/PROJECT_ID/secrets/trello-api-key/versions/latest,TRELLO_PASSWORD=projects/PROJECT_ID/secrets/trello-api-token/versions/latest" \
  --allow-unauthenticated
```

### Custom Deployment
```yaml
# cloudbuild.yaml customization
steps:
  - name: 'gcr.io/cloud-builders/docker'
    args: ['build', '--tag', 'gcr.io/$PROJECT_ID/trello-mcp:latest', '.']
    
  - name: 'gcr.io/google.com/cloudsdktool/cloud-sdk'
    args: [
      'run', 'deploy', 'trello-mcp',
      '--memory', '1Gi',           # Increase memory
      '--cpu', '2',                # Increase CPU
      '--concurrency', '100',      # Higher concurrency
      '--max-instances', '50'      # Scale limit
    ]
```

## 🧪 Testing

### Local Development
```bash
# Install dependencies
pip install -r requirements.txt

# Run locally
python main.py

# Test endpoints
curl http://localhost:8080/health
curl -X POST http://localhost:8080/mcp \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","method":"tools/list","id":1}'
```

### Validation Script
```python
# test_imports.py - verify all components load
import sys
import asyncio

async def test_server():
    try:
        from main import app
        from tools import TrelloTools
        
        tools = TrelloTools()
        available_tools = tools.get_tools()
        
        print(f"✅ Server loaded successfully")
        print(f"✅ {len(available_tools)} tools registered")
        
        expected_tools = [
            "list_boards", "get_board", "create_board", "update_board",
            "get_lists", "create_list", "get_cards", "create_card", 
            "update_card", "add_member_to_card", "search_cards"
        ]
        
        for tool in expected_tools:
            if tool in available_tools:
                print(f"✅ {tool}")
            else:
                print(f"❌ {tool} missing")
                
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(test_server())
```

## 🆘 Troubleshooting

### Common Issues

**"Import could not be resolved"**
```bash
# Install dependencies
pip install -r requirements.txt
```

**"Unauthorized - check your API key and token"**
```bash
# Verify credentials at https://trello.com/app-key
# Ensure token is not expired
# Check API key format (32 characters)
```

**"Rate limit exceeded"** 
```bash
# Server automatically handles rate limiting
# Wait 10 seconds and retry
# Consider reducing request frequency
```

**Build fails on Cloud Run**
```bash
# Check billing is enabled
gcloud billing accounts list

# Verify APIs are enabled  
gcloud services enable run.googleapis.com cloudbuild.googleapis.com

# Check quotas
gcloud compute project-info describe --project=$PROJECT_ID
```

### Debug Mode
```bash
# Enable debug logging
export DEBUG=true
export LOG_LEVEL=DEBUG

python main.py
```

### Log Analysis
```bash
# View Cloud Run logs
gcloud run logs read trello-mcp --region=us-central1 --limit=50

# Filter for errors
gcloud run logs read trello-mcp --region=us-central1 | grep ERROR

# Real-time logs
gcloud run logs tail trello-mcp --region=us-central1
```

## 🤝 Contributing

### Development Setup
```bash
git clone <repository>
cd trello-mcp-server

# Create virtual environment
python -m venv venv
source venv/bin/activate  # or `venv\Scripts\activate` on Windows

# Install dependencies
pip install -r requirements.txt

# Run tests
python test_imports.py
```

### Code Style
- **PEP 8** compliant
- **Type hints** for all functions
- **Docstrings** for all modules and classes
- **Error handling** with specific exceptions

## 📄 License

MIT License - see LICENSE file for details.

## 🙋‍♂️ Support

- **Documentation**: Check `QUICKSTART.md` and `FILE_MANIFEST.md`
- **Issues**: Create GitHub issues for bugs/features
- **Architecture**: See `DEPLOYMENT_SUMMARY.md`

---

## 📚 Related Documentation

### Getting Started
- [START_HERE.txt](./START_HERE.txt) - First-time orientation
- [QUICKSTART.md](./QUICKSTART.md) - 5-minute deployment guide  
- [QUICK_START_LOGIN.txt](./QUICK_START_LOGIN.txt) - ⭐ NEW: 2-minute interactive login guide

### Interactive Login Feature (NEW!)
- [INTERACTIVE_LOGIN_GUIDE.md](./INTERACTIVE_LOGIN_GUIDE.md) - Complete guide with examples
- [LOGIN_FEATURE.md](./LOGIN_FEATURE.md) - Feature overview and benefits
- [FEATURE_SUMMARY.txt](./FEATURE_SUMMARY.txt) - Visual diagrams and implementation details

### Architecture & Deployment
- [DEPLOYMENT_SUMMARY.md](./DEPLOYMENT_SUMMARY.md) - Architecture deep dive
- [IMPLEMENTATION_SUMMARY.md](./IMPLEMENTATION_SUMMARY.md) - Implementation details
- [FILE_MANIFEST.md](./FILE_MANIFEST.md) - File-by-file breakdown

### Testing
- [TESTING_GUIDE.md](./TESTING_GUIDE.md) - Comprehensive testing guide

---

**Built with ❤️ for seamless Trello-AI integration**

🚀 **Ready to deploy? Start with `QUICKSTART.md`!**
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

## 🔗 Integration Examples

### Claude Desktop Configuration

Add to `claude_desktop_config.json`:
```json
{
  "mcpServers": {
    "trello": {
      "command": "node",
      "args": ["/path/to/trello-mcp-client.js"],
      "env": {
        "TRELLO_MCP_URL": "https://your-service-url"
      }
    }
  }
}
```

### Custom AI Agent Integration

```python
import aiohttp
import json

class TrelloMCPClient:
    def __init__(self, server_url, api_key, token):
        self.server_url = server_url
        self.api_key = api_key
        self.token = token
        
    async def call_tool(self, tool_name, **kwargs):
        payload = {
            "jsonrpc": "2.0",
            "method": "tools/call",
            "id": 1,
            "params": {
                "name": tool_name,
                "arguments": {
                    "api_key": self.api_key,
                    "token": self.token,
                    **kwargs
                }
            }
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.post(
                f"{self.server_url}/mcp",
                json=payload
            ) as response:
                return await response.json()
                
    async def list_boards(self):
        return await self.call_tool("list_boards")
        
    async def create_card(self, name, list_id, **kwargs):
        return await self.call_tool(
            "create_card", 
            name=name, 
            list_id=list_id, 
            **kwargs
        )
```

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

# Cloud Run auto-injected
K_SERVICE=trello-mcp
K_REVISION=trello-mcp-00001-abc
PORT=8080
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
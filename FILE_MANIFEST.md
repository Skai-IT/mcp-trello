# 📋 File Manifest - Trello MCP Server

This document explains what each file does in the Trello MCP server project. Perfect for understanding the codebase structure and making modifications.

## 🏗️ Core Application Files

### `main.py` (156 lines)
**Purpose**: HTTP server entry point for Google Cloud Run  
**What it does**:
- FastAPI application with CORS middleware
- Health check endpoint (`/health`) for monitoring
- MCP protocol endpoint (`/mcp`) for tool execution
- Graceful startup/shutdown with lifespan management
- Signal handling for clean termination
- Error handling with JSON-RPC error responses

**Key Functions**:
- `health_check()` - Cloud Run health monitoring
- `handle_mcp_request()` - Route MCP protocol calls
- `lifespan()` - Manage server lifecycle

### `mcp_server.py` (148 lines)
**Purpose**: Model Context Protocol implementation  
**What it does**:
- Handles JSON-RPC 2.0 protocol compliance
- Routes MCP method calls to appropriate handlers
- Manages server initialization and capabilities
- Provides tool listing and execution interfaces

**Key Methods**:
- `initialize()` - MCP server setup
- `handle_request()` - Route incoming MCP calls
- `_handle_tool_call()` - Execute specific tools
- `_handle_tools_list()` - Return available tools

### `trello_client.py` (340 lines)
**Purpose**: Comprehensive Trello API wrapper  
**What it does**:
- HTTP client with authentication and rate limiting
- All Trello API operations (boards, lists, cards)
- Error handling and response validation
- Rate limiter (300 requests per 10 seconds)

**Key Classes**:
- `TrelloClient` - Main API client
- `RateLimiter` - Enforce Trello's rate limits
- `TrelloAPIError` - Custom exception handling

### `tools.py` (522 lines)
**Purpose**: Implementation of all 11 MCP tools  
**What it does**:
- Defines tool schemas for MCP protocol
- Implements business logic for each Trello operation
- Input validation and credential checking
- Formats responses for AI agents

**The 11 Tools**:
1. `list_boards` - Get user's boards
2. `get_board` - Detailed board information
3. `create_board` - Create new board
4. `update_board` - Modify existing board
5. `get_lists` - Get board's lists
6. `create_list` - Create new list
7. `get_cards` - Get cards from board/list
8. `create_card` - Create new card
9. `update_card` - Modify existing card
10. `add_member_to_card` - Assign team member
11. `search_cards` - Search across boards

## 🔧 Configuration & Schemas

### `config.py` (22 lines)
**Purpose**: Environment configuration management  
**What it does**:
- Loads environment variables
- Cloud Run specific settings
- Debug and logging configuration
- Service metadata

**Key Settings**:
- `DEBUG` - Development mode
- `PORT` - Server port (default 8080)
- `SERVICE_NAME` - Cloud Run service name

### `logging_config.py` (47 lines)
**Purpose**: Structured logging for Cloud Run  
**What it does**:
- JSON formatted logs for Google Cloud Logging
- Custom formatter with timestamps and metadata
- Log level configuration
- Third-party library noise reduction

**Features**:
- Structured JSON output
- Cloud Run service metadata
- Request tracing capabilities

### `schemas.py` (40 lines)  
**Purpose**: Pydantic data models for type safety  
**What it does**:
- Input validation for all tool parameters
- Type definitions for API requests/responses
- Data sanitization and length limits
- Error messages for invalid inputs

**Key Models**:
- `TrelloCredentials` - API key and token
- `CreateBoardRequest` - Board creation parameters
- `CreateCardRequest` - Card creation parameters
- `UpdateCardRequest` - Card modification parameters

## 🚀 Deployment Files

### `Dockerfile` (Multi-stage build)
**Purpose**: Container image for Cloud Run deployment  
**What it does**:
- Multi-stage build for minimal image size (<200MB)
- Python 3.11 slim base image
- Virtual environment for dependencies
- Non-root user for security
- Health check configuration

**Build Stages**:
1. **Builder**: Install dependencies in virtual environment
2. **Production**: Copy only runtime requirements

### `cloudbuild.yaml`
**Purpose**: CI/CD pipeline for Google Cloud Build  
**What it does**:
- Build Docker image
- Push to Container Registry
- Deploy to Cloud Run with optimized settings
- Configure service parameters

**Deployment Settings**:
- Memory: 512Mi
- CPU: 1 vCPU
- Concurrency: 80
- Max instances: 100

### `requirements.txt`
**Purpose**: Python dependency specification  
**Dependencies**:
- `fastapi==0.104.1` - Web framework
- `uvicorn[standard]==0.24.0` - ASGI server
- `aiohttp==3.9.1` - HTTP client
- `pydantic==2.5.2` - Data validation

### `.dockerignore`
**Purpose**: Exclude files from Docker build context  
**Excludes**:
- Python cache files (`__pycache__`)
- Virtual environments (`venv/`)
- IDE files (`.vscode/`, `.idea/`)
- OS files (`.DS_Store`)
- Logs and temporary files

## 📚 Documentation Files

### `START_HERE.txt`
**Purpose**: Quick orientation for new users  
**What it provides**:
- Project overview and key features
- Quick start checklist
- Essential files to read
- Security highlights
- Cost information

### `QUICKSTART.md`
**Purpose**: 5-minute deployment guide  
**Step-by-step**:
1. Get Trello credentials (2 min)
2. Deploy to Cloud Run (3 min)
3. Test server endpoints
4. Integration examples

### `README.md`
**Purpose**: Comprehensive project documentation  
**Sections**:
- Feature overview
- Architecture explanation
- Usage examples
- Integration guides
- Troubleshooting
- API reference

### `DEPLOYMENT_SUMMARY.md`
**Purpose**: Architecture and deployment deep dive  
**Contents**:
- System architecture diagrams
- Security model explanation
- Performance characteristics
- Cost analysis
- Monitoring setup

### `FILE_MANIFEST.md` (This file)
**Purpose**: Explain what each file does  
**Helps with**:
- Understanding codebase structure
- Knowing which file to modify for changes
- Onboarding new developers

## 🧪 Testing & Validation

### `test_imports.py`
**Purpose**: Verify all components load correctly  
**What it tests**:
- Import all Python modules
- Initialize TrelloTools class
- Verify all 11 tools are registered
- Check for missing dependencies

**Usage**:
```bash
python test_imports.py
# Expected output:
# ✅ Server loaded successfully
# ✅ 11 tools registered
# ✅ list_boards
# ✅ get_board
# ... (all 11 tools)
```

## 🔄 File Dependencies

```
main.py
├── config.py
├── logging_config.py
└── mcp_server.py
    └── tools.py
        ├── schemas.py
        └── trello_client.py
            └── schemas.py

Dockerfile
├── requirements.txt
└── [all .py files]

cloudbuild.yaml
├── Dockerfile
└── [deployment config]
```

## 📊 File Size & Complexity

| File | Lines | Complexity | Purpose |
|------|-------|------------|---------|
| `tools.py` | 522 | High | Business logic implementation |
| `trello_client.py` | 340 | Medium | API client with rate limiting |
| `main.py` | 156 | Medium | HTTP server setup |
| `mcp_server.py` | 148 | Medium | MCP protocol handling |
| `logging_config.py` | 47 | Low | Logging configuration |
| `schemas.py` | 40 | Low | Data models |
| `config.py` | 22 | Low | Environment config |

## 🛠️ Modification Guide

### Adding a New Tool
**Files to modify**:
1. `trello_client.py` - Add API method if needed
2. `tools.py` - Add tool definition and implementation
3. `schemas.py` - Add request/response models if needed

### Changing Configuration
**Files to modify**:
1. `config.py` - Add new environment variables
2. `main.py` - Use new config in server setup
3. `cloudbuild.yaml` - Update deployment parameters

### Adding Security Features
**Files to modify**:
1. `schemas.py` - Add validation rules
2. `trello_client.py` - Enhance authentication
3. `main.py` - Add middleware or headers

### Improving Logging
**Files to modify**:
1. `logging_config.py` - Update log format
2. Any `.py` file - Add logging statements

### Deployment Changes
**Files to modify**:
1. `Dockerfile` - Change container setup
2. `cloudbuild.yaml` - Update CI/CD pipeline
3. `requirements.txt` - Add/update dependencies

## 🎯 Quick File Reference

**Need to...**
- **Add a tool**: `tools.py` + `schemas.py`
- **Fix API issue**: `trello_client.py`
- **Change server behavior**: `main.py`
- **Update deployment**: `cloudbuild.yaml`
- **Modify logging**: `logging_config.py`
- **Add validation**: `schemas.py`
- **Environment config**: `config.py`
- **Protocol handling**: `mcp_server.py`

## 📋 File Checklist for Production

**Before deploying, ensure**:
✅ All `.py` files have proper error handling  
✅ `requirements.txt` has pinned versions  
✅ `Dockerfile` uses non-root user  
✅ `config.py` has all needed environment variables  
✅ `tools.py` validates all inputs  
✅ `test_imports.py` passes successfully  
✅ Documentation is up to date  

---

**Total Project**: 18 files, ~1,300 lines of code, production-ready

🚀 **Now you know exactly what each file does! Ready to customize or deploy!**
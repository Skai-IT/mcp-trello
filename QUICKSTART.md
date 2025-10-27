# 🚀 Trello MCP Server - 5-Minute Quickstart

Deploy your Trello MCP server to Google Cloud Run in just 5 minutes!

## ⚡ Prerequisites

- Google Cloud Project with billing enabled
- `gcloud` CLI installed and authenticated
- Trello API credentials (get them below)

## 🔑 Step 1: Get Trello Credentials (2 minutes)

1. Go to: https://trello.com/app-key
2. **Copy your API Key** - you'll need this
3. **Generate a Token** by clicking the "Token" link
4. **Copy the Token** - you'll need this too

💡 **Keep these safe!** The server asks for them per-request (never stored).

## 🏗️ Step 2: Deploy to Cloud Run (3 minutes)

```bash
# 1. Navigate to the project directory
cd /Users/shlomisha/Documents/vscodeprojects/Trello

# 2. Set your Google Cloud project
export PROJECT_ID="your-gcp-project-id"
gcloud config set project $PROJECT_ID

# 3. Enable required APIs (if not already enabled)
gcloud services enable run.googleapis.com cloudbuild.googleapis.com

# 4. Build and push the Docker image
gcloud builds submit --tag gcr.io/$PROJECT_ID/trello-mcp:latest .

# 5. Deploy to Cloud Run
gcloud run deploy trello-mcp \
  --image gcr.io/$PROJECT_ID/trello-mcp:latest \
  --region us-central1 \
  --platform managed \
  --allow-unauthenticated \
  --memory 512Mi \
  --cpu 1 \
  --concurrency 80 \
  --max-instances 100 \
  --timeout 300 \
  --port 8080
```

## ✅ Step 3: Get Your Server URL

```bash
# Get the deployed service URL
gcloud run services describe trello-mcp \
  --region us-central1 \
  --format='value(status.url)'
```

**Save this URL!** You'll use it to integrate with AI agents.

## 🧪 Step 4: Test Your Server

```bash
# Replace with your actual URL
export SERVER_URL="https://trello-mcp-xxxxx-uc.a.run.app"

# Test health check
curl $SERVER_URL/health

# Test MCP initialization
curl -X POST $SERVER_URL/mcp \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "method": "initialize",
    "id": 1,
    "params": {
      "protocolVersion": "2024-11-05",
      "capabilities": {},
      "clientInfo": {"name": "test", "version": "1.0.0"}
    }
  }'

# List available tools
curl -X POST $SERVER_URL/mcp \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "method": "tools/list",
    "id": 2
  }'
```

Expected response: JSON with 11 Trello tools listed.

## 🎯 Step 5: Integrate with AI Agents

### For Claude Desktop:

Add to your `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "trello": {
      "command": "curl",
      "args": [
        "-X", "POST",
        "https://your-trello-mcp-url/mcp",
        "-H", "Content-Type: application/json",
        "-d", "@-"
      ],
      "disabled": false
    }
  }
}
```

### For Custom Integration:

Use the MCP protocol endpoints:
- **Initialize**: `POST /mcp` with `initialize` method
- **List Tools**: `POST /mcp` with `tools/list` method  
- **Call Tool**: `POST /mcp` with `tools/call` method

## 🔧 Tool Usage Examples

### List Boards
```json
{
  "jsonrpc": "2.0",
  "method": "tools/call",
  "id": 3,
  "params": {
    "name": "list_boards",
    "arguments": {
      "api_key": "your-trello-api-key",
      "token": "your-trello-token"
    }
  }
}
```

### Create Board
```json
{
  "jsonrpc": "2.0", 
  "method": "tools/call",
  "id": 4,
  "params": {
    "name": "create_board",
    "arguments": {
      "api_key": "your-trello-api-key",
      "token": "your-trello-token",
      "name": "My New Board",
      "desc": "Created via MCP server"
    }
  }
}
```

### Search Cards
```json
{
  "jsonrpc": "2.0",
  "method": "tools/call", 
  "id": 5,
  "params": {
    "name": "search_cards",
    "arguments": {
      "api_key": "your-trello-api-key",
      "token": "your-trello-token",
      "query": "urgent",
      "limit": 20
    }
  }
}
```

## 🎉 Success! 

Your Trello MCP server is now live and ready to use!

**What you accomplished:**
✅ Deployed production-ready MCP server  
✅ 11 Trello tools available
✅ Secure credential handling
✅ Rate limiting and error handling
✅ Health monitoring

## 📋 All Available Tools

| Tool | Description |
|------|-------------|
| `list_boards` | List all user boards |
| `get_board` | Get detailed board info |
| `create_board` | Create new board |
| `update_board` | Update existing board |
| `get_lists` | Get lists from board |
| `create_list` | Create new list |
| `get_cards` | Get cards from board/list |
| `create_card` | Create new card |
| `update_card` | Update existing card |
| `add_member_to_card` | Assign member to card |
| `search_cards` | Search cards across boards |

## 💰 Costs

**Expected monthly cost: ~$1-2**
- Cloud Run: 2M free requests/month
- Container Registry: ~$0.40/month
- Logging: ~$1/month

## 🆘 Troubleshooting

**Build fails?**
- Check that billing is enabled
- Verify `gcloud` is authenticated: `gcloud auth list`

**Deploy fails?**
- Ensure APIs are enabled: `gcloud services list --enabled`
- Check region is supported: `gcloud run regions list`

**Tools not working?**
- Verify Trello credentials at https://trello.com/app-key
- Check API key and token are not expired

**Need help?** 
- Check the full README.md for detailed documentation
- Review logs: `gcloud run logs read trello-mcp --region us-central1`

---

🎯 **Ready to build amazing Trello integrations!**
## 🔐 Interactive Login Feature

The Trello MCP Server now supports **interactive, session-based credential management**. You no longer need to manually provide your API key and token with every request!

### How It Works

1. **First Request**: When you call any tool without providing credentials, the system will:
   - Open your browser to `https://trello.com/app-key`
   - Prompt you to enter your API Key and Token in the terminal
   - Cache your credentials for the session (8 hours by default)

2. **Subsequent Requests**: Your credentials are automatically used from the session cache
   - No need to enter them again
   - No credentials stored on disk
   - Credentials cleared when the session ends

### Example Usage

#### Request 1: Search for your Cisco IronPort card (First time - will prompt)
```json
{
  "jsonrpc": "2.0",
  "method": "tools/call",
  "id": 1,
  "params": {
    "name": "search_cards",
    "arguments": {
      "query": "Cisco IronPort"
    }
  }
}
```

**What happens:**
1. Browser opens to https://trello.com/app-key
2. Terminal prompts you to enter API Key
3. Terminal prompts you to enter Token
4. Credentials are cached
5. Card search executes and returns results

#### Request 2: List your boards (Subsequent request - uses cached credentials)
```json
{
  "jsonrpc": "2.0",
  "method": "tools/call",
  "id": 2,
  "params": {
    "name": "list_boards",
    "arguments": {}
  }
}
```

**What happens:**
1. Uses cached credentials automatically
2. Lists all your boards immediately
3. No prompts needed

### Features

✅ **Interactive Browser-Based Login**
- Automatically opens `https://trello.com/app-key` in your browser
- No need to manually navigate

✅ **Session Caching**
- Credentials cached for 8 hours (configurable)
- Credentials cleared when session ends
- No persistent storage on disk

✅ **Backward Compatible**
- You can still provide credentials with requests if you prefer
- Provided credentials override cached ones
- Mixed approach supported

✅ **Secure**
- Credentials only in memory during session
- No files written to disk
- Separate session per MCP server instance

### Terminal Prompt Example

When you make your first request, you'll see:

```
============================================================
🔐 TRELLO LOGIN REQUIRED
============================================================

Please authenticate with Trello:

1. A browser window will open to https://trello.com/app-key
2. Copy your API Key (shown at the top)
3. Click 'Token' link to generate/view your Token
4. Return here and paste both values

------------------------------------------------------------

📋 Enter your Trello API Key: [paste your key here]
🔑 Enter your Trello Token: [paste your token here]

✅ Credentials received and cached for this session

============================================================
```

### Configuration

Edit `credential_manager.py` to customize:

```python
# Cache duration (default: 480 minutes = 8 hours)
credential_manager = CredentialManager(cache_duration_minutes=480)
```

### API Key Sources

- **API Key & Token**: https://trello.com/app-key
- Click "Token" link to generate or view your token
- Keep these private and never share them

### Troubleshooting

**"Browser didn't open"**
- Manually visit https://trello.com/app-key
- Copy your API Key and Token
- Paste them when prompted in the terminal

**"Credentials expired"**
- Just call a tool again and you'll be prompted to log in again
- Default cache duration is 8 hours

**"Wrong credentials entered"**
- You'll see an error message
- The next tool call will prompt you to login again
- Double-check your API Key and Token at https://trello.com/app-key

### Session Management

The credential manager is initialized per MCP server instance:

```python
# In tools.py
self.credential_manager = CredentialManager()
```

This means:
- Each server instance has its own credential cache
- Multiple server instances can run with different credentials
- Restarting the server clears all cached credentials

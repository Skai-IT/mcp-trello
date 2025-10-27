# 🔐 Interactive Login - Complete Usage Guide

## Overview

Your Trello MCP Server now has **interactive, session-based credential management**. This means:

✅ **First request**: Browser opens, you enter credentials  
✅ **Subsequent requests**: Credentials cached automatically  
✅ **Secure**: No persistent storage, only in-memory session cache  
✅ **Flexible**: Still supports providing credentials directly if needed  

---

## Quick Start

### Example: Search for your Cisco IronPort card

**Request:**
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
1. ✅ Browser automatically opens to `https://trello.com/app-key`
2. ✅ Terminal shows login prompt:
   ```
   ============================================================
   🔐 TRELLO LOGIN REQUIRED
   ============================================================
   
   📋 Enter your Trello API Key: [you paste here]
   🔑 Enter your Trello Token: [you paste here]
   
   ✅ Credentials received and cached for this session
   ============================================================
   ```
3. ✅ Search executes and returns your Cisco IronPort cards

### Next request (automatic)

**Request:**
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
- ✅ Uses cached credentials automatically
- ✅ No prompts, instant execution
- ✅ No need to provide API key/token

---

## How to Get Your Credentials

### Step 1: Visit Trello App Key Page
Go to: **https://trello.com/app-key**

You'll see:
```
Key
[Your API Key Here] ← Copy this
```

### Step 2: Generate/View Your Token
On the same page, click the **"Token"** link

You'll see:
```
Token
[Your API Token Here] ← Copy this
```

### Step 3: Use Them in the MCP
When prompted by the MCP server:
```
📋 Enter your Trello API Key: [paste here]
🔑 Enter your Trello Token: [paste here]
```

---

## Advanced Usage

### Option 1: Interactive (Recommended)
Just provide the query without credentials - server will prompt:

```json
{
  "params": {
    "name": "search_cards",
    "arguments": {
      "query": "Cisco IronPort"
    }
  }
}
```

### Option 2: Provide Credentials Explicitly
Override cached credentials:

```json
{
  "params": {
    "name": "search_cards",
    "arguments": {
      "api_key": "your-api-key",
      "token": "your-token",
      "query": "Cisco IronPort"
    }
  }
}
```

### Option 3: Mixed (Hybrid)
Session cache as fallback:

```json
{
  "params": {
    "name": "search_cards",
    "arguments": {
      "query": "Cisco IronPort"
      // api_key and token optional - will use cache
    }
  }
}
```

---

## Session Management

### How Long Do Credentials Stay Cached?
**Default: 8 hours**

After 8 hours:
- Cache expires automatically
- Next tool call will prompt you to login again
- You'll see the login prompt again

### How to Clear Cache Early
Restart the MCP server:
```bash
# Stop the server and start it again
# All cached credentials are cleared
```

### Can I Use Multiple Trello Accounts?
Yes! Run separate MCP server instances:

```bash
# Server 1 - Account A
gcloud run deploy trello-mcp-1 --source .

# Server 2 - Account B  
gcloud run deploy trello-mcp-2 --source .
```

Each server maintains its own credential cache.

---

## Real-World Examples

### Example 1: Search for Card (No Credentials Provided)

```json
{
  "jsonrpc": "2.0",
  "method": "tools/call",
  "id": 1,
  "params": {
    "name": "search_cards",
    "arguments": {
      "query": "Cisco IronPort",
      "limit": 10
    }
  }
}
```

**Terminal Output:**
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

📋 Enter your Trello API Key: _
```

**You enter:**
- API Key: `abc123...` (from Trello)
- Token: `xyz789...` (from Trello)

**Server response:**
```json
{
  "content": [{
    "type": "text",
    "text": "Found 2 Cisco IronPort cards:\n\n1. Cisco IronPort Email Gateway\n2. Cisco IronPort Configuration"
  }]
}
```

### Example 2: List Boards (Uses Cache Automatically)

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

**Terminal Output:**
```
(no prompts - uses cached credentials)
```

**Server response:**
```json
{
  "content": [{
    "type": "text",
    "text": "Your Trello boards:\n\n1. Work Projects\n2. Personal Tasks\n3. Team Collaboration"
  }]
}
```

### Example 3: Create Board (With Explicit Credentials)

```json
{
  "jsonrpc": "2.0",
  "method": "tools/call",
  "id": 3,
  "params": {
    "name": "create_board",
    "arguments": {
      "api_key": "different-key",
      "token": "different-token",
      "name": "New Board",
      "desc": "A fresh board"
    }
  }
}
```

**Terminal Output:**
```
(ignores cache, uses provided credentials)
```

---

## API Endpoint Reference

### Check Login URL
```bash
GET /auth/login

Response:
{
  "message": "Interactive login will be triggered on first tool call",
  "login_url": "https://trello.com/app-key",
  "instructions": {...},
  "features": {
    "automatic_browser_open": true,
    "session_caching": true,
    "cache_duration_minutes": 480
  }
}
```

### List Available Tools
```bash
GET /tools

Response:
{
  "tools": [...],
  "count": 11
}
```

Note: All 11 tools now have optional `api_key` and `token` fields

---

## Troubleshooting

### Issue: "Browser didn't open automatically"
**Solution:**
- Manually visit: https://trello.com/app-key
- When you press Enter at the terminal, it will wait for your credentials
- Paste API Key and Token as shown

### Issue: "Invalid credentials error"
**Solution:**
1. Go to https://trello.com/app-key again
2. Double-check your API Key and Token
3. Try again - the system will prompt you to login again

### Issue: "I want to login with a different account"
**Solution:**
1. Restart the MCP server (clears cache)
2. Make a tool call
3. You'll be prompted to login again
4. Use the new account credentials

### Issue: "Cache expired, need to login again"
**Solution:**
- This happens after 8 hours of caching
- Just call a tool again when needed
- You'll be prompted to login
- To change this duration, edit `credential_manager.py` line ~14

### Issue: "Can I use credentials with Claude Desktop?"
**Solution:**
Yes! The interactive login works with Claude Desktop MCP:
1. Configure in `claude_desktop_config.json` to point to your MCP server
2. First interaction will trigger the browser login
3. Subsequent interactions use cache
4. You only need to login once per 8-hour session

---

## Environment Variables

The credential manager doesn't use environment variables by design (more secure).

However, you can customize the cache duration in `credential_manager.py`:

```python
# Change this line to adjust cache duration
self.credential_manager = CredentialManager(cache_duration_minutes=480)
# Default: 480 minutes (8 hours)
# Examples: 60 (1 hour), 240 (4 hours), 1440 (24 hours)
```

---

## Security Details

✅ **Never stored to disk**
- Credentials only in memory during session
- No files written to ~/.trello or similar
- No config files contain credentials

✅ **Per-instance caching**
- Each MCP server instance has its own cache
- Multiple instances = multiple separate caches
- No cross-instance credential sharing

✅ **Session-based**
- Cleared on server restart
- Cleared after 8 hours of inactivity
- Manually clearable by restarting

✅ **No third-party storage**
- Credentials never sent anywhere except Trello's official API
- No cloud logging of credentials
- No analytics platforms involved

---

## Testing the Feature

### Test 1: Initial Login
```bash
curl -X POST https://your-mcp-url/mcp \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "method": "tools/call",
    "id": 1,
    "params": {
      "name": "list_boards",
      "arguments": {}
    }
  }'
```

Expected: Browser opens, terminal prompts for credentials

### Test 2: Cached Credentials
```bash
curl -X POST https://your-mcp-url/mcp \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "method": "tools/call",
    "id": 2,
    "params": {
      "name": "search_cards",
      "arguments": {
        "query": "test"
      }
    }
  }'
```

Expected: No browser, no prompts, instant result (uses cache)

### Test 3: Override Cache
```bash
curl -X POST https://your-mcp-url/mcp \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "method": "tools/call",
    "id": 3,
    "params": {
      "name": "list_boards",
      "arguments": {
        "api_key": "different-key",
        "token": "different-token"
      }
    }
  }'
```

Expected: Uses provided credentials, ignores cache

---

## Summary

| Feature | Before | After |
|---------|--------|-------|
| Credentials | Had to provide with every request | Enter once, auto-cached |
| Browser | Manual visit to Trello | Automatic browser open |
| Prompts | None (had to pass manually) | User-friendly terminal prompts |
| Security | Mixed (files, env vars) | Session-only, in-memory |
| Cache | None | 8-hour automatic cache |
| Multiple accounts | Not supported | Separate server instances |

---

## Next Steps

1. ✅ Try your first search: 
   ```json
   {
     "name": "search_cards",
     "arguments": {"query": "Cisco IronPort"}
   }
   ```

2. ✅ Get your Trello credentials from https://trello.com/app-key

3. ✅ When prompted, paste them

4. ✅ Enjoy cached credentials for your session!

**That's it! No more manual credential management.** 🎉

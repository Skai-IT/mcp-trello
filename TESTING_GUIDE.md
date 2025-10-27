# 🧪 Testing Trello MCP in Cloud Run from VS Code

This guide walks you through testing your live Trello MCP server in Google Cloud Run using VS Code's REST Client extension.

## 📦 Prerequisites

### 1. Install REST Client Extension for VS Code
- **Extension**: REST Client by Huachao Mao
- **ID**: `humao.rest-client`
- Install from VS Code Extensions marketplace

**Steps:**
1. Open VS Code
2. Go to Extensions (Cmd+Shift+X on Mac)
3. Search for "REST Client"
4. Click Install on the one by Huachao Mao

### 2. Get Your Trello Credentials
1. Go to: https://trello.com/app-key
2. **Copy your API Key** (32 characters)
3. Click "Token" link to generate a token
4. **Copy your Token** (long string)
5. Keep these safe!

---

## 🚀 How to Test

### Step 1: Open the Test File

```
/Users/shlomisha/Documents/vscodeprojects/Trello/test-cloud-run.http
```

**In VS Code:**
1. Open the file: `Cmd+P` → type `test-cloud-run.http`
2. Or navigate: `File → Open` → find the file

### Step 2: Add Your Credentials

Look for this section in the file (around line 45):
```
@apiKey = YOUR_TRELLO_API_KEY_HERE
@token = YOUR_TRELLO_TOKEN_HERE
```

**Replace with your actual credentials:**
```
@apiKey = abc1234567890def1234567890abcdef
@token = ATTAxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

### Step 3: Run Tests

Each request has a **"Send Request"** link that appears when you hover over the line number.

**Test Order:**

#### 🟢 Start with Basic Tests (No Credentials Needed)

1. **Health Check** - Verify service is running
   - Click "Send Request" on request #1
   - Should return: `{"status":"healthy",...}`

2. **Server Info** - Get server details
   - Click "Send Request" on request #2
   - Shows service name and version

3. **List Tools** - See all 11 available tools
   - Click "Send Request" on request #3
   - Lists all tool names and schemas

#### 🔵 Continue with MCP Protocol Tests

4. **MCP Initialize** - Start MCP session
   - Click "Send Request" on request #4
   - Initializes the protocol

5. **List Tools via MCP** - Get tools list via protocol
   - Click "Send Request" on request #5
   - Shows all 11 tools in MCP format

#### 🟡 Test with Credentials (Requires Trello API Key + Token)

6. **List Boards** - Get all your Trello boards
   - Click "Send Request" on request #6
   - Shows all boards you have access to

7. **Create Board** - Create a new test board
   - Click "Send Request" on request #8
   - Creates "Test Board from VS Code"
   - **Note:** You'll need the board_id for later tests

8. **Other Tests** - Use board_id from previous result
   - For get_board, get_lists, etc., replace `REPLACE_WITH_BOARD_ID`
   - Copy the board ID from the previous response
   - Replace in the request body

---

## 📝 Request Templates

### Template 1: Simple Tool Call
```http
POST {{baseUrl}}/mcp
Content-Type: {{contentType}}

{
  "jsonrpc": "2.0",
  "method": "tools/call",
  "id": 1,
  "params": {
    "name": "TOOL_NAME",
    "arguments": {
      "api_key": "{{apiKey}}",
      "token": "{{token}}",
      "param1": "value1"
    }
  }
}
```

### Template 2: Custom Request
1. Copy any request from the file
2. Modify the `params` section with your data
3. Click "Send Request"

---

## 🔍 Understanding Responses

### Success Response
```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": {
    "content": [{
      "type": "text",
      "text": "✅ Board created successfully!..."
    }]
  }
}
```

### Error Response
```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "error": {
    "code": -32603,
    "message": "Unauthorized - check your API key and token",
    "data": "..."
  }
}
```

---

## 💡 Pro Tips

### Tip 1: Copy Response Data
- Click the **Copy** button on the response
- Paste into your requests for IDs
- Makes testing sequential operations easier

### Tip 2: Use Variables
You can add custom variables at the top of the file:
```http
@boardId = 123abc456def789ghi
@listId = 987ijk654lmn321opq
```

Then use them in requests:
```json
"board_id": "{{boardId}}"
```

### Tip 3: Check Logs While Testing
In a terminal, watch Cloud Run logs:
```bash
gcloud run logs tail trello-mcp --region=us-central1 --project=kenshoo-it-dept
```

### Tip 4: Save Test Sequences
Create multiple `.http` files for different test scenarios:
- `test-boards.http` - Board operations
- `test-cards.http` - Card operations
- `test-search.http` - Search operations

---

## 🐛 Troubleshooting

### Issue: "Connection refused"
**Solution**: Verify the service URL is correct
```
https://trello-mcp-116435607783.us-central1.run.app
```

### Issue: "Unauthorized - check your API key and token"
**Solution**: 
1. Go to https://trello.com/app-key
2. Verify API key is correct
3. Check token is not expired
4. Make sure you didn't accidentally include spaces

### Issue: "Invalid board_id"
**Solution**:
1. First run "List Boards" request (#6)
2. Copy the `id` field from a board in the response
3. Replace `REPLACE_WITH_BOARD_ID` with actual ID

### Issue: REST Client extension not showing "Send Request"
**Solution**:
1. Install REST Client extension
2. Restart VS Code
3. Make sure file is named `*.http`

---

## 🎯 Recommended Test Flow

1. ✅ Health Check (verify service is up)
2. ✅ Server Info (verify version)
3. ✅ List Tools (verify 11 tools available)
4. ✅ MCP Initialize (start protocol session)
5. ✅ List Boards (verify credentials work)
6. ✅ Create Board (test write operations)
7. ✅ Get Board (test read operations)
8. ✅ Get Lists (test nested operations)
9. ✅ Create Card (test complex operations)
10. ✅ Search Cards (test search operations)

---

## 📊 Example Workflow

**Step-by-step example:**

1. Add your credentials to the file
2. Run "Health Check" → ✅ Should show healthy
3. Run "List Tools" → ✅ Should show 11 tools
4. Run "List Boards" → ✅ Should show your boards
5. Copy a board ID from the response
6. Edit "Get Board" request, replace `REPLACE_WITH_BOARD_ID`
7. Run "Get Board" → ✅ Should show board details
8. Edit "Get Lists" request, paste the same board ID
9. Run "Get Lists" → ✅ Should show lists on that board
10. Continue testing other operations!

---

## 🔗 Resources

- **REST Client Extension**: https://github.com/Huachao/vscode-restclient
- **Trello API Docs**: https://developer.atlassian.com/cloud/trello/rest/api-group-boards/
- **JSON-RPC 2.0 Spec**: https://www.jsonrpc.org/specification

---

## ✨ Next Steps

After successful testing:

1. **Document Results** - Save responses showing tests pass
2. **Integrate with Agents** - Use service URL with your AI agents
3. **Monitor Logs** - Check Cloud Run logs regularly
4. **Explore Tools** - Try all 11 tools with different parameters
5. **Share Results** - Show team the working integration

---

**Happy testing! 🎉**

Questions? Check the main README.md or DEPLOYMENT_NOTES.md in the repository!
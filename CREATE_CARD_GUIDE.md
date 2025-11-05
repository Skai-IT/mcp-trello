# 📋 Create a New Trello Card - Complete Guide

## 🎯 Quick Start (2 minutes)

### What You Need
1. **Trello API credentials** (from https://trello.com/app-key)
2. **Board ID** - ID of the board where you want the card
3. **List ID** - ID of the list where the card should go

### Required Information
- **name** - Title of the card (required)
- **list_id** - Which list to add the card to (required)

### Optional Information
- **desc** - Description of the card
- **due** - Due date (ISO format: "2025-12-31")
- **labels** - Label IDs to add to the card
- **members** - Member IDs to assign to the card
- **pos** - Position in the list

---

## 📝 Step 1: Get Your Board and List IDs

### Using Claude Desktop or VS Code

**List your boards:**
```
"List my Trello boards"
```

**Output example:**
```
Board: "Project Alpha" (ID: 5f4c1a2b3c4d5e6f)
Board: "Team Tasks" (ID: 6g5d2b3c4e5f6g7h)
```

**Get lists from a board:**
```
"Show me the lists on the 'Project Alpha' board"
```

**Output example:**
```
List: "To Do" (ID: 5f4c1a2b3c4d5e6f)
List: "In Progress" (ID: 5f4c1a2b3c4d5e7g)
List: "Done" (ID: 5f4c1a2b3c4d5e8h)
```

---

## 🚀 Step 2: Create the Card

### Using the MCP Tools

The `create_card` tool requires:
- `name` - Card title
- `list_id` - List ID where the card goes

### Via Claude Desktop/VS Code

**Simple card (title only):**
```
Create a new card in my "To Do" list with the title "Fix bug #123"
```

**Card with description:**
```
Create a card titled "Design new dashboard" in the "Project Alpha" board's "In Progress" list with description "Focus on mobile responsiveness"
```

**Card with due date:**
```
Create a card "Q1 Planning Meeting" in the "Team Tasks" board with a due date of December 15, 2025
```

**Card with all details:**
```
Create a card titled "Security Audit" 
Description: "Review API endpoints and database security"
In list: "Project Alpha" > "In Progress"
Due date: January 31, 2025
Assign to: [team member emails]
Labels: "critical", "security"
```

---

## 🔧 Step 3: Using the API Directly

### Python Example

```python
import httpx
import asyncio
from datetime import datetime, timedelta

async def create_trello_card():
    """Create a new Trello card"""
    
    client = httpx.AsyncClient()
    
    # Your credentials (set as environment variables)
    api_key = "your-api-key"
    token = "your-api-token"
    
    # Card details
    card_data = {
        "name": "Review code changes",
        "list_id": "5f4c1a2b3c4d5e6f",  # List ID
        "desc": "Review PR #456 for backend changes",
        "due": (datetime.now() + timedelta(days=3)).isoformat(),
        "labels": ["urgent", "review"],
        "members": ["user_id_1", "user_id_2"]
    }
    
    # Call the MCP server
    response = await client.post(
        "http://localhost:8080/mcp",
        json={
            "jsonrpc": "2.0",
            "id": 1,
            "method": "tools/call",
            "params": {
                "name": "create_card",
                "arguments": {
                    "api_key": api_key,
                    "token": token,
                    **card_data
                }
            }
        }
    )
    
    result = response.json()
    print(f"Card created: {result}")
    
# Run it
asyncio.run(create_trello_card())
```

### JavaScript/Node.js Example

```javascript
const fetch = require('node-fetch');

async function createTrelloCard() {
    const apiKey = 'your-api-key';
    const token = 'your-api-token';
    const listId = '5f4c1a2b3c4d5e6f';
    
    const cardData = {
        name: 'Review code changes',
        list_id: listId,
        desc: 'Review PR #456 for backend changes',
        due: new Date(Date.now() + 3 * 24 * 60 * 60 * 1000).toISOString(),
        labels: ['urgent', 'review'],
        members: ['user_id_1', 'user_id_2']
    };
    
    const response = await fetch('http://localhost:8080/mcp', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            jsonrpc: '2.0',
            id: 1,
            method: 'tools/call',
            params: {
                name: 'create_card',
                arguments: {
                    api_key: apiKey,
                    token: token,
                    ...cardData
                }
            }
        })
    });
    
    const result = await response.json();
    console.log('Card created:', result);
}

createTrelloCard();
```

### cURL Example

```bash
# Create a simple card
curl -X POST http://localhost:8080/mcp \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "id": 1,
    "method": "tools/call",
    "params": {
      "name": "create_card",
      "arguments": {
        "api_key": "YOUR_API_KEY",
        "token": "YOUR_API_TOKEN",
        "name": "Review code changes",
        "list_id": "5f4c1a2b3c4d5e6f",
        "desc": "Review PR #456",
        "due": "2025-12-31T23:59:59Z"
      }
    }
  }'
```

---

## 📋 Card Parameters Reference

| Parameter | Type | Required | Description | Example |
|-----------|------|----------|-------------|---------|
| `name` | String | ✅ Yes | Card title | "Fix login bug" |
| `list_id` | String | ✅ Yes | List ID | "5f4c1a2b3c4d5e6f" |
| `desc` | String | ❌ No | Card description | "Update auth middleware" |
| `due` | String | ❌ No | Due date (ISO 8601) | "2025-12-31T23:59:59Z" |
| `labels` | Array | ❌ No | Label names | ["bug", "urgent"] |
| `members` | Array | ❌ No | Member IDs | ["user1", "user2"] |
| `pos` | String/Number | ❌ No | Card position | "top", "bottom", or number |
| `api_key` | String | ✅ Yes | Your API key | From https://trello.com/app-key |
| `token` | String | ✅ Yes | Your API token | From https://trello.com/app-key |

---

## 🔍 Finding List IDs

### Method 1: Using the MCP Tools (Easiest)

```
"What lists are in my board named 'My Board'?"
```

### Method 2: Trello Web
1. Go to your board
2. Open browser console (F12)
3. Run: `fetch('/1/members/me/boards?lists=open').then(r=>r.json()).then(b=>b[0].lists.forEach(l=>console.log(l.name, l.id)))`

### Method 3: Trello API
```bash
curl "https://api.trello.com/1/boards/{BOARD_ID}/lists?key={API_KEY}&token={TOKEN}"
```

---

## 💡 Common Use Cases

### Quick Task Card
```python
{
    "name": "Update documentation",
    "list_id": "LIST_ID_TODO",
    "desc": "Add API examples to README"
}
```

### Urgent Bug Report
```python
{
    "name": "Critical: Database connection timeout",
    "list_id": "LIST_ID_BUG",
    "desc": "Users unable to login. Started 2 hours ago.",
    "due": "2025-12-26T08:00:00Z",  # Tomorrow morning
    "labels": ["critical", "bug", "p0"]
}
```

### Team Task with Assignments
```python
{
    "name": "Sprint Planning Meeting",
    "list_id": "LIST_ID_EVENTS",
    "desc": "Discuss goals and priorities for next sprint",
    "due": "2025-12-27T14:00:00Z",  # Friday 2 PM
    "members": ["alice_id", "bob_id", "charlie_id"]
}
```

### Feature Request with Details
```python
{
    "name": "Add dark mode support",
    "list_id": "LIST_ID_FEATURES",
    "desc": """## Overview
Add dark mode theme to improve user experience for low-light environments

## Acceptance Criteria
- [ ] Toggle in user settings
- [ ] Persists across sessions  
- [ ] Works on mobile
- [ ] WCAG compliant

## Resources
- [Design mockups](link)
- [Dark mode guidelines](link)""",
    "due": "2026-01-15T23:59:59Z",
    "labels": ["feature", "ui", "enhancement"]
}
```

---

## ✅ Verification

### After Creating a Card

1. **Check Trello Web**
   - Go to your board
   - Find the card in the correct list
   - Verify all details are correct

2. **Check via MCP**
   ```
   "Show me cards in the 'To Do' list of my board"
   ```

3. **Look for your new card**
   - It should appear in the results
   - All details should match what you entered

---

## 🐛 Troubleshooting

### Problem: "Invalid list_id"
- ✅ Make sure the list_id is correct (not the board_id)
- ✅ Verify the list belongs to a board you have access to
- ✅ Check that you're using the right API credentials

### Problem: "Card creation failed"
- ✅ Check your API key and token are valid
- ✅ Verify the list_id exists
- ✅ Check card name is not empty
- ✅ Verify due date is in ISO format if provided

### Problem: "Card created but not visible"
- ✅ Refresh the Trello page (F5)
- ✅ Check you're looking at the correct list
- ✅ Verify the card wasn't added to a different list
- ✅ Check board permissions

### Problem: "Members not assigned"
- ✅ Verify member IDs are correct
- ✅ Members must be part of the board
- ✅ Use email addresses if member IDs don't work

---

## 🚀 Advanced: Create Multiple Cards

### Using Python Loop
```python
cards_to_create = [
    {"name": "Task 1", "list_id": "LIST_ID"},
    {"name": "Task 2", "list_id": "LIST_ID"},
    {"name": "Task 3", "list_id": "LIST_ID"},
]

async def create_multiple_cards():
    for card in cards_to_create:
        await create_trello_card(**card)
```

### Using Batch Request
```python
# Create multiple cards in sequence
tasks = [
    create_card("Card A", list_id_1),
    create_card("Card B", list_id_2),
    create_card("Card C", list_id_1),
]

await asyncio.gather(*tasks)
```

---

## 📚 Related Commands

- **List boards:** `list_boards` - See all your boards
- **Get lists:** `get_lists` - See lists in a board
- **Get cards:** `get_cards` - See cards in a list
- **Update card:** `update_card` - Modify existing card
- **Add member:** `add_member_to_card` - Assign people to card
- **Search cards:** `search_cards` - Find specific cards

---

## 🔗 Resources

- [Trello API Documentation](https://developer.atlassian.com/cloud/trello/rest/api-group-cards/)
- [Get Your Credentials](https://trello.com/app-key)
- [Integration Guide](./INTEGRATION_GUIDE.md)
- [MCP Server Documentation](./README.md)


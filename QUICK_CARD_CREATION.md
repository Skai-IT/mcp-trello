# ⚡ Quick Card Creation - Step by Step

## 🎯 The Simplest Way: Using Claude Desktop or VS Code

### Step 1: Get Your Credentials ✅
Visit: https://trello.com/app-key
- Copy your **API Key** (top of page)
- Click **Token** and copy it
- Done! You have what you need

### Step 2: Get Board and List IDs ✅
**Ask Claude/VS Code:**
```
"List my Trello boards"
```

**Look for your board in the output, note the ID. Then ask:**
```
"Show me the lists in my 'Project Alpha' board"
```

**Look for the list where you want the card, note its ID**

### Step 3: Create the Card ✅
**Simple version - just title and list:**
```
Create a card titled "My New Task" in my "To Do" list
```

**With description:**
```
Create a card titled "Fix login bug"
Description: "Users unable to login on mobile"
Add to: "Project Alpha" board, "In Progress" list
```

**With all details:**
```
Create a card titled "Design API endpoints"
Description: "Create REST API spec for v2 release"
Add to: "Development" board, "In Progress" list
Due date: December 31, 2025
```

---

## 📝 Example Conversation Flow

### Your Request:
> "Help me create a card in Trello for a task called 'Review Database Schema'"

### Claude's Response:
> "I'll help you create that card! First, I need to know which board and list you'd like it in. Let me show you your boards..."

### Claude Lists Your Boards:
```
Board: "Q4 Project" (ID: 5abc123)
Board: "Team Tasks" (ID: 6def456)
```

### You Choose:
> "Add it to the 'Team Tasks' board, in the 'To Do' list"

### Claude Shows Lists:
```
List: "To Do" (ID: 5zyx789)
List: "In Progress" (ID: 6wvu654)
List: "Done" (ID: 7tuv321)
```

### Claude Creates the Card:
> "Perfect! Creating your card 'Review Database Schema' in the 'To Do' list..."

```
✅ Card Created Successfully!

Card: Review Database Schema
Board: Team Tasks
List: To Do
Created: December 26, 2025
Status: Ready
```

---

## 🔑 Key Information to Gather

Before creating a card, you'll need:

| Item | Where to Find | Example |
|------|---------------|---------|
| API Key | https://trello.com/app-key | `abc123def456ghi789...` |
| Token | https://trello.com/app-key (click "Token") | `jkl012mno345pqr678...` |
| Board ID | Ask Claude "List my boards" | `5abc123` |
| List ID | Ask Claude "Show lists in [board]" | `5zyx789` |
| Card Title | Your choice | `"Review Database Schema"` |

---

## 💻 Using the MCP Server Directly

### If You Have Terminal Access

**Start the server:**
```bash
cd /Users/shlomisha/Documents/vscodeprojects/Trello
python main.py
```

**Server will start at: http://localhost:8080**

**Then use any method to call `create_card`:**
- Claude Desktop (recommended)
- VS Code with Cline extension
- Python script
- JavaScript/Node.js
- cURL

---

## 🎯 Common Scenarios

### Scenario 1: Create Bug Report Card
```
Tell Claude: "Create a bug report card for a crash on login. 
Title: 'Critical: Login Crash on iOS'
Description: 'Users unable to login on iOS 14+, shows blank screen'
Add to: 'Bugs' board, 'Critical' list
Mark due: Today + 1 day"
```

### Scenario 2: Create Feature Request
```
Tell Claude: "Create a feature card for dark mode.
Title: 'Add Dark Mode Support'
Description: 'Users request dark theme for evening use'
Add to: 'Features' board, 'Backlog' list
Due: End of month"
```

### Scenario 3: Create Team Task
```
Tell Claude: "Create a meeting card.
Title: 'Team Standup'
Description: '9 AM daily standup meeting'
Add to: 'Team' board, 'Meetings' list
Due: Tomorrow 9 AM
Assign to: [team members]"
```

### Scenario 4: Create Sprint Task
```
Tell Claude: "Create sprint card.
Title: 'Implement User Authentication'
Description: '[Include detailed requirements]'
Add to: 'Sprint' board, 'In Progress' list
Due: End of sprint
Assign team members"
```

---

## ✅ What Happens After Creation

1. **Card Appears in Trello**
   - Check your board
   - Refresh if needed
   - Card should be in the correct list

2. **You Can Edit It**
   - Add comments
   - Attach files
   - Change due date
   - Move to different list
   - Assign members

3. **Team Can See It**
   - If board is shared
   - Members see notifications
   - Can comment and collaborate

---

## 🆘 Need Help?

**"I don't know my board ID"**
→ Ask Claude: "What are my Trello boards?"

**"I don't know my list ID"**
→ Ask Claude: "Show me the lists in my [board name] board"

**"The card didn't create"**
→ Check: Do you have valid API key and token?
→ Check: Is the list_id correct?
→ Check: Is the card title provided?

**"I can't find the new card"**
→ Refresh your Trello page
→ Check you're looking at the right list
→ Check the card isn't in a different list

---

## 📚 Next Steps

1. **Read the Full Guide:** [CREATE_CARD_GUIDE.md](./CREATE_CARD_GUIDE.md)
2. **Get Credentials:** Visit https://trello.com/app-key
3. **Get Board/List IDs:** Use Claude to list your boards and lists
4. **Create Your First Card:** Use Claude, VS Code, or the API
5. **View on Trello:** Check your card appears correctly

---

## 🚀 Ready to Start?

**Option 1: Use Claude Desktop (Easiest)**
1. Open Claude Desktop
2. Ask: "List my Trello boards"
3. Ask: "Create a card titled 'My Task' in [board name] board, [list name] list"
4. Done!

**Option 2: Use VS Code (With Cline)**
1. Install Cline extension in VS Code
2. Same steps as Claude Desktop
3. Can also see responses in VS Code

**Option 3: Use Python Script**
See CREATE_CARD_GUIDE.md for complete Python example

**Option 4: Use cURL**
See CREATE_CARD_GUIDE.md for complete cURL example

---

Pick your method and let's create a card! 🎉


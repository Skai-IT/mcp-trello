# 🚀 Run the Interactive Card Creator NOW

## Quick Start (2 minutes)

### Step 1: Get Your Trello Credentials

1. Open: https://trello.com/app-key
2. Copy your **API Key** (top of page)
3. Click **"Token"** link
4. Copy your **Token**
5. Keep these ready!

### Step 2: Start the MCP Server

Open Terminal 1:
```bash
cd /Users/shlomisha/Documents/vscodeprojects/Trello
python main.py
```

**You should see:**
```
INFO:     Uvicorn running on http://127.0.0.1:8080
```

Keep this terminal open!

### Step 3: Run the Card Creator

Open Terminal 2:
```bash
cd /Users/shlomisha/Documents/vscodeprojects/Trello
python create_card_interactive.py
```

### Step 4: Follow the Prompts

```
→ Enter your Trello API Key: [paste your API key]
→ Enter your Trello Token: [paste your token]
```

Then:
- Select your board (1, 2, 3, etc.)
- Select your list (1, 2, 3, etc.)
- Enter card title (required)
- Enter description (optional - press Enter to skip)
- Enter due date (optional - format: YYYY-MM-DD)
- Enter labels (optional - comma-separated)

### Step 5: Check Your Trello Board

✅ You should see your new card in Trello!

---

## 📋 Example: Creating a Card

**Terminal 1 (Server):**
```bash
$ python main.py
INFO:     Uvicorn running on http://127.0.0.1:8080
INFO:     Application startup complete
```

**Terminal 2 (Card Creator):**
```bash
$ python create_card_interactive.py

============================================================
  🎯 TRELLO MCP - INTERACTIVE CARD CREATOR
============================================================

============================================================
  🔐 TRELLO CREDENTIALS
============================================================

Get your credentials from: https://trello.com/app-key

→ Enter your Trello API Key: abc123def456ghi789jkl012mno345pqr678stu901
✅ Credentials received!

============================================================
  📋 SELECT BOARD
============================================================

ℹ️  Fetching your boards...

Your boards:

  1. Personal Tasks (ID: 5f4c1a2b3c4d5e6f)
  2. Work Projects (ID: 5g5d2b3c4e5f6g7h)
  3. Team Board (ID: 5h6e3c4d5f6g7h8i)

→ Select board number: 1
✅ Selected: Personal Tasks

============================================================
  📝 SELECT LIST
============================================================

Board: Personal Tasks

ℹ️  Fetching lists from board 5f4c1a2b3c4d5e6f...

Lists:

  1. To Do (ID: 5i7f4d5e6g7h8i9j)
  2. In Progress (ID: 5j8g5e6f7h8i9j0k)
  3. Done (ID: 5k9h6f7g8i9j0k1l)

→ Select list number: 1
✅ Selected: To Do

============================================================
  🎫 CARD DETAILS
============================================================

→ Card title/name: Fix login authentication
→ Card description (optional, press Enter to skip): Users unable to login with SSO on mobile devices
→ Due date (YYYY-MM-DD format) (optional, press Enter to skip): 2025-12-27
→ Labels (comma-separated) (optional, press Enter to skip): bug, critical, mobile

============================================================
  ✨ RESULT
============================================================

✅ Card created successfully!

Card Details:
  • ID: 5l0i7g8h9j0k1l2m
  • Name: Fix login authentication
  • Board: 5f4c1a2b3c4d5e6f
  • List: 5i7f4d5e6g7h8i9j
  • Description: Users unable to login with SSO on mobile devices
  • Due: 2025-12-27T23:59:59Z
  • URL: https://trello.com/c/5l0i7g8h9j0k1l2m/42-fix-login-authentication

============================================================
  ✅ CARD CREATION COMPLETE
  Check your Trello board to see the new card!
============================================================
```

**Trello Board:**
You'll see your card "Fix login authentication" in the To Do list with:
- ✅ Description visible
- ✅ Due date set to Dec 27, 2025
- ✅ Labels: bug, critical, mobile

---

## 🔧 Troubleshooting

### "Cannot connect to MCP server"
Make sure Terminal 1 is running the server:
```bash
python main.py
```

The server must be running at `http://localhost:8080`

### "Error getting boards - Invalid credentials"
1. Check your API Key is correct
2. Check your Token is correct
3. Visit https://trello.com/app-key to verify
4. Try again with correct credentials

### "Card creation failed"
Check:
- [ ] Board was selected correctly
- [ ] List was selected correctly
- [ ] Card title is not empty
- [ ] Date format is YYYY-MM-DD (if provided)

### "Python: command not found"
Use:
```bash
python3 main.py
python3 create_card_interactive.py
```

---

## 📝 What You Can Do

With the interactive card creator, you can create cards with:

**Required:**
- Card title

**Optional:**
- Description (multi-line text)
- Due date (YYYY-MM-DD format)
- Labels (comma-separated)

**Example cards:**

1. **Simple task:**
   - Title: "Buy milk"
   - (Skip everything else)

2. **Bug report:**
   - Title: "Login fails on Safari"
   - Description: "Users with iOS 14+ cannot login"
   - Due: 2025-12-26
   - Labels: bug, critical

3. **Feature request:**
   - Title: "Add dark mode"
   - Description: "Users request dark theme for evening use"
   - Due: 2026-01-15
   - Labels: feature, ui

4. **Meeting:**
   - Title: "Team standup"
   - Description: "Daily 9 AM sync"
   - Due: 2025-12-26
   - Labels: meeting, daily

---

## 💡 Tips

1. **Keep credentials safe**
   - Never commit API key/token to version control
   - Don't share with others
   - Regenerate if you think they're compromised

2. **Use labels wisely**
   - Create consistent labels in Trello first
   - Examples: bug, feature, urgent, review, blocked

3. **Due dates**
   - Format must be: YYYY-MM-DD
   - Examples: 2025-12-31, 2026-01-15
   - Invalid format? Script will skip it

4. **Board/List selection**
   - Can't edit once selected
   - Script shows board/list IDs
   - Note them for future reference

---

## 🎉 Ready?

1. Get your credentials: https://trello.com/app-key
2. Terminal 1: `python main.py`
3. Terminal 2: `python create_card_interactive.py`
4. Follow the prompts
5. Check your Trello board!

Let's create your first card! 🚀

---

## 📖 Related Files

- **create_card_interactive.py** - The interactive script
- **CREATE_CARD_GUIDE.md** - Full documentation
- **QUICK_CARD_CREATION.md** - Quick reference
- **README.md** - Main MCP documentation


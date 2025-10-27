# Environment Variables - Quick Reference

## New Environment Variables

### `TRELLO_USERNAME`
- **Type:** String
- **Optional:** Yes
- **Default:** `None`
- **Description:** Trello API key/username for pre-configured authentication
- **Example:** `TRELLO_USERNAME=abc123xyz...`

### `TRELLO_PASSWORD`
- **Type:** String
- **Optional:** Yes
- **Default:** `None`
- **Description:** Trello API token/password for pre-configured authentication
- **Example:** `TRELLO_PASSWORD=def456uvw...`

---

## ⚡ Quick Setup Examples

### Cloud Run (5 seconds)
```bash
gcloud run deploy trello-mcp \
  --source . \
  --set-env-vars="TRELLO_USERNAME=your-api-key,TRELLO_PASSWORD=your-api-token" \
  --allow-unauthenticated
```

### Docker (5 seconds)
```bash
docker run -e TRELLO_USERNAME=your-api-key \
           -e TRELLO_PASSWORD=your-api-token \
           -p 8080:8080 trello-mcp:latest
```

### Local Development (interactive)
```bash
python main.py
# Will prompt for credentials on first use
```

### Local Development (pre-configured)
```bash
export TRELLO_USERNAME=your-api-key
export TRELLO_PASSWORD=your-api-token
python main.py
```

---

## 🔑 Getting Your Credentials

1. Visit: https://trello.com/app-key
2. Copy **API Key** (top of page)
3. Click **Token** link
4. Copy your **Token**

Both should be long strings (32+ characters)

---

## ✅ Verification

### Check if environment variables are set
```bash
echo $TRELLO_USERNAME
echo $TRELLO_PASSWORD
```

### Test the server
```bash
# Server should start without prompts if env vars are set
python main.py

# Should see: "Loading credentials from environment variables"
```

---

## 📚 Full Documentation

For complete documentation, see:
- [ENV_VARIABLES.md](./ENV_VARIABLES.md) - Comprehensive guide
- [README.md](./README.md#environment-variables) - Overview
- [INTEGRATION_GUIDE.md](./INTEGRATION_GUIDE.md) - Integration setup


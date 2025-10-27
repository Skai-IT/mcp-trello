# Environment Variables Configuration

This document describes all environment variables available for the Trello MCP server.

## Overview

The Trello MCP server supports configuration through environment variables. These variables can be set when deploying to Cloud Run, Docker, or running locally.

---

## Server Configuration Variables

### `PORT`
- **Type:** Integer
- **Default:** `8080`
- **Description:** Port on which the HTTP server listens
- **Example:** `PORT=8080`

### `DEBUG`
- **Type:** Boolean
- **Default:** `false`
- **Description:** Enable debug logging
- **Example:** `DEBUG=true`

### `LOG_LEVEL`
- **Type:** String
- **Default:** `INFO`
- **Options:** `DEBUG`, `INFO`, `WARNING`, `ERROR`, `CRITICAL`
- **Description:** Logging level for the application
- **Example:** `LOG_LEVEL=DEBUG`

### `REQUEST_TIMEOUT`
- **Type:** Integer (seconds)
- **Default:** `30`
- **Description:** HTTP request timeout duration
- **Example:** `REQUEST_TIMEOUT=60`

### `MAX_RETRIES`
- **Type:** Integer
- **Default:** `3`
- **Description:** Maximum number of retries for failed requests
- **Example:** `MAX_RETRIES=5`

---

## Credentials Configuration Variables

### `TRELLO_USERNAME`
- **Type:** String
- **Default:** `None` (optional)
- **Description:** Trello API username or identifier. When set along with `TRELLO_PASSWORD`, credentials are automatically loaded at startup without requiring interactive login.
- **Example:** `TRELLO_USERNAME=your-api-key`
- **Use Case:** Pre-configured authentication for non-interactive deployments (Cloud Run, Docker)
- **Security Note:** Use Cloud Run Secrets or Docker secrets, never commit to version control

### `TRELLO_PASSWORD`
- **Type:** String
- **Default:** `None` (optional)
- **Description:** Trello API token or password. Must be used together with `TRELLO_USERNAME`. When both are provided, credentials are cached for the session on startup.
- **Example:** `TRELLO_PASSWORD=your-api-token`
- **Use Case:** Pre-configured authentication for non-interactive deployments
- **Security Note:** Use Cloud Run Secrets or Docker secrets, never commit to version control

---

## Usage Examples

### Example 1: Local Development (Interactive Login)
```bash
# Run without credentials - will prompt for login when needed
DEBUG=true LOG_LEVEL=DEBUG python main.py
```

### Example 2: Cloud Run Deployment (Pre-configured Credentials)
```bash
# Deploy with pre-configured credentials
gcloud run deploy trello-mcp \
  --source . \
  --region us-central1 \
  --set-env-vars="TRELLO_USERNAME=your-api-key,TRELLO_PASSWORD=your-api-token" \
  --allow-unauthenticated
```

### Example 3: Docker Container (Pre-configured Credentials)
```bash
# Run Docker container with environment variables
docker run -e TRELLO_USERNAME=your-api-key \
           -e TRELLO_PASSWORD=your-api-token \
           -e PORT=8080 \
           -p 8080:8080 \
           trello-mcp:latest
```

### Example 4: Cloud Run with Secrets (Recommended)
```bash
# Create secrets in Google Cloud
gcloud secrets create trello-username --replication-policy="automatic" --data-file=- <<< "your-api-key"
gcloud secrets create trello-password --replication-policy="automatic" --data-file=- <<< "your-api-token"

# Deploy with secret references
gcloud run deploy trello-mcp \
  --source . \
  --region us-central1 \
  --set-env-vars="TRELLO_USERNAME=projects/PROJECT_ID/secrets/trello-username/versions/latest,TRELLO_PASSWORD=projects/PROJECT_ID/secrets/trello-password/versions/latest" \
  --allow-unauthenticated
```

### Example 5: Docker Compose with Secrets
```yaml
version: '3.8'

services:
  trello-mcp:
    image: trello-mcp:latest
    ports:
      - "8080:8080"
    environment:
      - TRELLO_USERNAME=your-api-key
      - TRELLO_PASSWORD=your-api-token
      - LOG_LEVEL=INFO
      - DEBUG=false
    secrets:
      - trello_username
      - trello_password

secrets:
  trello_username:
    file: ./secrets/username.txt
  trello_password:
    file: ./secrets/password.txt
```

---

## Credential Loading Priority

The credential manager loads credentials in the following priority order:

1. **Environment Variables** - If `TRELLO_USERNAME` and `TRELLO_PASSWORD` are set, they are loaded at startup
2. **Function Parameters** - If credentials are passed to individual tool functions
3. **Session Cache** - If credentials were cached from a previous call in this session
4. **Interactive Prompt** - If no credentials found above, user is prompted to enter them interactively

Example flow:
```python
# This priority order is used when calling any tool:
def get_or_prompt_credentials(api_key, token):
    # 1. Use provided function parameters
    if api_key and token:
        return (api_key, token)
    
    # 2. Use cached credentials from session
    cached = get_cached_credentials()
    if cached:
        return cached
    
    # 3. Use environment variables (loaded in __init__)
    if self.env_username and self.env_password:
        return (self.env_username, self.env_password)
    
    # 4. Prompt user interactively
    return prompt_for_credentials()
```

---

## Cloud Run Deployment

### Using Cloud Run Secrets (Recommended)

#### Step 1: Create secrets
```bash
# From command line
gcloud secrets create trello-api-key \
  --replication-policy="automatic" \
  --data-file=- <<< "your-actual-api-key"

gcloud secrets create trello-api-token \
  --replication-policy="automatic" \
  --data-file=- <<< "your-actual-api-token"

# Verify secrets were created
gcloud secrets list
```

#### Step 2: Deploy with secrets
```bash
gcloud run deploy trello-mcp \
  --source . \
  --region us-central1 \
  --allow-unauthenticated \
  --cpu-boost \
  --memory 512Mi \
  --timeout 300 \
  --set-env-vars="TRELLO_USERNAME=projects/PROJECT_ID/secrets/trello-api-key/versions/latest,TRELLO_PASSWORD=projects/PROJECT_ID/secrets/trello-api-token/versions/latest"
```

### Getting Your Project ID
```bash
# Find your project ID
gcloud config get-value project

# Output: kenshoo-it-dept (or your project ID)

# Use it in deployment
gcloud run deploy trello-mcp \
  --set-env-vars="TRELLO_USERNAME=projects/kenshoo-it-dept/secrets/trello-api-key/versions/latest,TRELLO_PASSWORD=projects/kenshoo-it-dept/secrets/trello-api-token/versions/latest"
```

---

## Docker Deployment

### Using Docker Environment Variables

#### Step 1: Create .env file
```bash
# .env file
TRELLO_USERNAME=your-api-key
TRELLO_PASSWORD=your-api-token
LOG_LEVEL=INFO
DEBUG=false
PORT=8080
```

#### Step 2: Build and run
```bash
# Build
docker build -t trello-mcp:latest .

# Run with .env file
docker run --env-file .env -p 8080:8080 trello-mcp:latest

# Or set environment variables directly
docker run \
  -e TRELLO_USERNAME=your-api-key \
  -e TRELLO_PASSWORD=your-api-token \
  -e LOG_LEVEL=INFO \
  -p 8080:8080 \
  trello-mcp:latest
```

---

## Local Development

### Option 1: Interactive Login (Default)
```bash
# Run without credentials - will prompt when needed
python main.py
# The server will prompt for credentials when first tool is called
```

### Option 2: Environment Variables
```bash
# Set environment variables
export TRELLO_USERNAME=your-api-key
export TRELLO_PASSWORD=your-api-token

# Run server
python main.py
```

### Option 3: .env File
```bash
# Create .env file
cat > .env << EOF
TRELLO_USERNAME=your-api-key
TRELLO_PASSWORD=your-api-token
LOG_LEVEL=DEBUG
DEBUG=true
EOF

# Run with env variables loaded (requires python-dotenv)
pip install python-dotenv
python -m dotenv run python main.py
```

---

## Security Best Practices

### ❌ DO NOT:
- Commit credentials to version control
- Use credentials in plaintext in Docker files
- Log credentials in debug output
- Share credentials in URLs or parameters

### ✅ DO:
- Use Cloud Run Secrets for production
- Use Docker secrets for Docker Compose
- Use .env files only in local development
- Rotate credentials regularly
- Use API keys with limited permissions
- Audit access logs for suspicious activity

### Environment Variable Security Example
```bash
# ❌ WRONG: Credentials in Dockerfile
FROM python:3.11
ENV TRELLO_USERNAME=abc123xyz
ENV TRELLO_PASSWORD=def456uvw

# ✅ CORRECT: Credentials from build args or secrets
FROM python:3.11
ARG TRELLO_USERNAME
ARG TRELLO_PASSWORD
ENV TRELLO_USERNAME=${TRELLO_USERNAME}
ENV TRELLO_PASSWORD=${TRELLO_PASSWORD}

# ✅ EVEN BETTER: Cloud Run secrets or Docker secrets
```

---

## Troubleshooting

### Issue: Credentials not loading
```bash
# Verify environment variables are set
echo $TRELLO_USERNAME
echo $TRELLO_PASSWORD

# Check if both are required
# TRELLO_USERNAME and TRELLO_PASSWORD must BOTH be set
# If only one is set, the other will be used as None
```

### Issue: "Invalid credentials" error
```bash
# Verify credentials are valid Trello API credentials
# 1. Visit https://trello.com/app-key
# 2. Copy API Key (32+ character string)
# 3. Click "Token" to generate/view token
# 4. Verify credentials are at least 32 characters each

# Re-export with correct values
export TRELLO_USERNAME=correct-api-key
export TRELLO_PASSWORD=correct-token
```

### Issue: Cloud Run deployment fails
```bash
# Check if secrets exist
gcloud secrets list

# Verify secret content is correct
gcloud secrets versions access latest --secret=trello-api-key

# Check if project ID is correct in env var
gcloud config get-value project
```

---

## Environment Variable Reference Table

| Variable | Type | Default | Required | Example | Use Case |
|----------|------|---------|----------|---------|----------|
| `PORT` | Integer | `8080` | No | `8080` | Server port |
| `DEBUG` | Boolean | `false` | No | `true` | Debug logging |
| `LOG_LEVEL` | String | `INFO` | No | `DEBUG` | Log verbosity |
| `REQUEST_TIMEOUT` | Integer | `30` | No | `60` | Request timeout |
| `MAX_RETRIES` | Integer | `3` | No | `5` | Retry attempts |
| `TRELLO_USERNAME` | String | `None` | No* | `api-key-123` | Pre-configured auth |
| `TRELLO_PASSWORD` | String | `None` | No* | `token-456` | Pre-configured auth |

*Note: `TRELLO_USERNAME` and `TRELLO_PASSWORD` must be set together. If only one is provided, it will be ignored and interactive login will be used.

---

## Next Steps

- [Integration Guide](INTEGRATION_GUIDE.md) - Set up with Claude Desktop, VS Code, etc.
- [Quick Start](QUICKSTART.md) - Get started quickly
- [Architecture](ARCHITECTURE.md) - Understand the system design


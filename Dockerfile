# Multi-stage Dockerfile optimized for Google Cloud Run
FROM python:3.11-slim as builder

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
  PYTHONUNBUFFERED=1 \
  PIP_NO_CACHE_DIR=1 \
  PIP_DISABLE_PIP_VERSION_CHECK=1

# Install system dependencies
RUN apt-get update && apt-get install -y \
  gcc \
  && rm -rf /var/lib/apt/lists/*

# Create virtual environment
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Copy and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Production stage
FROM python:3.11-slim as production

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
  PYTHONUNBUFFERED=1 \
  PATH="/opt/venv/bin:$PATH"

# Copy virtual environment from builder stage
COPY --from=builder /opt/venv /opt/venv

# Create non-root user
RUN useradd --create-home --shell /bin/bash app

# Set working directory
WORKDIR /app

# Copy application code
COPY main.py .
COPY mcp_server.py .
COPY trello_client.py .
COPY tools.py .
COPY schemas.py .
COPY config.py .
COPY logging_config.py .
COPY credential_manager.py .

# Change ownership to non-root user
RUN chown -R app:app /app
USER app

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD python -c "import requests; requests.get('http://localhost:8080/health', timeout=5)"

# Expose port
EXPOSE 8080

# Run the application
CMD ["python", "main.py"]
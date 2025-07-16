# Use Python 3.12 slim image
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Create non-root user for security
RUN groupadd -r emotilang && useradd -r -g emotilang emotilang

# Install system dependencies
RUN apt-get update && apt-get install -y \
    --no-install-recommends \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and gunicorn config
COPY requirements.txt .

# Install Python dependencies
COPY sly/ sly/
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install ./sly

# Copy source code
COPY src/ src/

# Create temp directory with proper permissions
RUN mkdir -p /tmp/emotilang && chown emotilang:emotilang /tmp/emotilang

# Set proper permissions
RUN chown -R emotilang:emotilang /app

# Switch to non-root user
USER emotilang

# Set environment variables
ENV PYTHONPATH=/app/src:/app/sly/src
ENV FLASK_APP=src/web/server.py
ENV FLASK_ENV=production

# Expose port
EXPOSE 8080

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8080/ || exit 1

# Run the application with Gunicorn
CMD ["gunicorn", "--chdir", "src/web", "--config", "src/web/gunicorn.conf.py", "wsgi:app"]

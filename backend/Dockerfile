FROM python:3.11-alpine

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app

# Install system dependencies including FFmpeg libraries for aiortc
RUN apk add --no-cache \
    libpq \
    postgresql-dev \
    gcc \
    musl-dev \
    libffi-dev \
    openssl-dev \
    ffmpeg-dev \
    && rm -rf /var/cache/apk/*

# Create app directory
WORKDIR /app

# Create non-root user
RUN adduser -D -s /bin/sh appuser

# Copy requirements and install Python dependencies
COPY requirements-prod.txt .
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements-prod.txt

# Copy only necessary application code
COPY app/ ./app/
COPY start.sh .
RUN chmod +x start.sh

# Change ownership to non-root user
RUN chown -R appuser:appuser /app

# Switch to non-root user
USER appuser

# Expose port
EXPOSE 8000

# Healthcheck
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD wget --spider -q http://localhost:${PORT:-8000}/health || exit 1

# Run the application
CMD ["sh", "./start.sh"]
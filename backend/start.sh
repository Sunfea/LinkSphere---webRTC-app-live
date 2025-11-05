#!/bin/bash

# Production startup script for WebRTC Backend

echo "Starting WebRTC Backend..."

# Run database migrations
echo "Running database migrations..."
alembic upgrade head

# Start the application with production settings
echo "Starting Uvicorn server..."
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
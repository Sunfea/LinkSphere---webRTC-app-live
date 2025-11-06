#!/bin/sh

# Production startup script for WebRTC Backend

echo "Starting WebRTC Backend..."

# Wait for database to be ready
echo "Waiting for database to be ready..."
until alembic upgrade head
do
  echo "Database not ready, waiting..."
  sleep 5
done

echo "Database migrations completed successfully!"

# Start the application with production settings
echo "Starting Uvicorn server..."
uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000} --workers 4
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
from app.api.api_new import api_router
from app.signaling.server import signaling_app
from app.core.database import engine, Base
import uvicorn

# Create database tables (handle errors gracefully)
try:
    Base.metadata.create_all(bind=engine)
except Exception as e:
    print(f"Warning: Could not create database tables: {e}")

app = FastAPI(
    title="WebRTC Video/Audio Communication App",
    description="A real-time video/audio communication backend using WebRTC",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(api_router, prefix="/api")

# Mount the signaling app for WebSocket connections
app.mount("/ws", signaling_app)

@app.get("/")
async def root():
    return {"message": "WebRTC Video/Audio Communication Backend"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    uvicorn.run(
        "main_new:app",
        host=os.getenv("HOST", "0.0.0.0"),
        port=int(os.getenv("PORT", 8000)),
        reload=os.getenv("DEBUG", "False").lower() == "true",
        log_level="info"
    )
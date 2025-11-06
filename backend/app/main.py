from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os
from pathlib import Path
from app.api.api_new import api_router
from app.api.routes import router as legacy_router
from app.api.metrics import router as metrics_router, track_request_metrics
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

# Add metrics middleware
@app.middleware("http")
async def add_metrics_middleware(request, call_next):
    return await track_request_metrics(request, call_next)

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
app.include_router(legacy_router, prefix="/api/legacy")
app.include_router(metrics_router, prefix="/api")

# Mount the signaling app for WebSocket connections
app.mount("/ws", signaling_app)

# Serve frontend static files
# In Docker, frontend is copied to /app/frontend
# In development, it's in the project root
frontend_path = Path("/app/frontend")
print(f"Looking for frontend at: {frontend_path}")
print(f"Frontend path exists: {frontend_path.exists()}")

if frontend_path.exists():
    print(f"Mounting static files from: {frontend_path}")
    app.mount("/static", StaticFiles(directory=str(frontend_path)), name="static")

# Serve the main index.html file
@app.get("/")
async def read_index():
    index_path = frontend_path / "index.html"
    print(f"Looking for index.html at: {index_path}")
    print(f"Index path exists: {index_path.exists()}")
    if index_path.exists():
        return FileResponse(index_path)
    return {"message": "WebRTC Video/Audio Communication Backend"}

# Serve frontend HTML files directly
@app.get("/login")
async def read_login():
    login_path = frontend_path / "login.html"
    if login_path.exists():
        return FileResponse(login_path)
    return {"message": "Login page not found"}

@app.get("/signup")
async def read_signup():
    signup_path = frontend_path / "signup.html"
    if signup_path.exists():
        return FileResponse(signup_path)
    return {"message": "Signup page not found"}

@app.get("/dashboard")
async def read_dashboard():
    dashboard_path = frontend_path / "dashboard.html"
    if dashboard_path.exists():
        return FileResponse(dashboard_path)
    return {"message": "Dashboard page not found"}

@app.get("/room")
async def read_room():
    room_path = frontend_path / "room.html"
    if room_path.exists():
        return FileResponse(room_path)
    return {"message": "Room page not found"}

@app.get("/username")
async def read_username():
    username_path = frontend_path / "username.html"
    if username_path.exists():
        return FileResponse(username_path)
    return {"message": "Username page not found"}

@app.get("/verify")
async def read_verify():
    verify_path = frontend_path / "verify.html"
    if verify_path.exists():
        return FileResponse(verify_path)
    return {"message": "Verify page not found"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "version": "1.0.0"}

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=os.getenv("HOST", "0.0.0.0"),
        port=int(os.getenv("PORT", 8000)),
        reload=os.getenv("DEBUG", "False").lower() == "true",
        log_level="info"
    )
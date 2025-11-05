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

# Serve static files
# In Docker: /app/frontend, Local: parent.parent.parent / "frontend"
frontend_path = Path("/app/frontend") if Path("/app/frontend").exists() else Path(__file__).parent.parent.parent / "frontend"
if frontend_path.exists():
    app.mount("/static", StaticFiles(directory=frontend_path), name="static")

# Include API routes
app.include_router(api_router, prefix="/api")
app.include_router(legacy_router, prefix="/api/legacy")
app.include_router(metrics_router, prefix="/api")

# Mount the signaling app for WebSocket connections
app.mount("/ws", signaling_app)

# Serve frontend pages
# In Docker: /app/frontend, Local: parent.parent.parent / "frontend"
frontend_path = Path("/app/frontend") if Path("/app/frontend").exists() else Path(__file__).parent.parent.parent / "frontend"

@app.get("/")
@app.head("/")
async def serve_index():
    return FileResponse(frontend_path / "index.html")

@app.get("/signup")
@app.head("/signup")
async def serve_signup():
    return FileResponse(frontend_path / "signup.html")

@app.get("/verify")
@app.head("/verify")
async def serve_verify():
    return FileResponse(frontend_path / "verify.html")

@app.get("/username")
@app.head("/username")
async def serve_username():
    return FileResponse(frontend_path / "username.html")

@app.get("/login")
@app.head("/login")
async def serve_login():
    return FileResponse(frontend_path / "login.html")

@app.get("/dashboard")
@app.head("/dashboard")
async def serve_dashboard():
    return FileResponse(frontend_path / "dashboard.html")

@app.get("/room")
@app.head("/room")
async def serve_room():
    return FileResponse(frontend_path / "room.html")

@app.get("/404")
@app.head("/404")
async def serve_404():
    return FileResponse(frontend_path / "404.html")

@app.get("/test")
async def serve_test():
    return FileResponse(frontend_path / "test.html")

@app.get("/test-dashboard")
async def serve_test_dashboard():
    return FileResponse(frontend_path / "test-dashboard.html")

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
# Premium WebRTC Video Calling Application

A modern, real-time video conferencing application built with FastAPI and WebRTC technology.

Live - https://linksphere-webrtc-app-2-production.up.railway.app/

## 🚀 Features

- **HD Video Calls** - Crystal-clear 1080p video with adaptive quality
- **Secure & Private** - End-to-end encryption with JWT authentication
- **Real-time Communication** - Ultra-low latency peer-to-peer connections
- **Room Management** - Create, join, and manage video rooms
- **Premium Dark UI** - Modern, responsive interface with glassmorphism effects
- **Multi-participant Support** - Multiple users can join the same room
- **Email Verification** - Secure OTP-based user registration

## 📋 Prerequisites

- Python 3.8+
- Modern web browser (Chrome, Firefox, Safari, Edge)
- Docker & Docker Compose (recommended)
- PostgreSQL (for production)

## 🛠️ Installation

### 1. Clone the Repository

```bash
git clone <your-repo-url>
cd webRTC
```

### 2. Set Up Backend

```bash
# Using Docker (recommended)
docker-compose up --build

# Or manually:
cd backend
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate

# Install dependencies
pip install -r requirements-prod.txt
```

### 3. Configure Environment Variables

```bash
# Copy example environment file
cp .env.example .env

# Edit .env and update with your settings
# IMPORTANT: Change SECRET_KEY in production!
```

### 4. Initialize Database

```bash
# Database migrations are automatically applied on startup
# Or manually run migrations:
alembic upgrade head
```

## 🚀 Running the Application

### Using Docker (Recommended)

```bash
# Build and start all services
docker-compose up --build

# Run in detached mode
docker-compose up -d --build
```

### Development Mode

```bash
cd backend
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

### Production Mode

```bash
cd backend
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

## 🌐 Access the Application

Open your browser and navigate to:
- **Frontend**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs

## 📁 Project Structure

```
webRTC/
├── backend/
│   ├── app/               # Backend application code
│   │   ├── api/           # API endpoints
│   │   ├── core/          # Core configurations
│   │   ├── models/        # Database models
│   │   ├── schemas/       # Pydantic schemas
│   │   ├── signaling/     # WebSocket signaling
│   │   └── utils/         # Utility functions
│   ├── alembic/           # Database migrations
│   ├── requirements.txt   # Python dependencies
│   ├── requirements-prod.txt # Production dependencies
│   └── Dockerfile
├── frontend/              # Frontend files
│   ├── css/               # Stylesheets
│   ├── js/                # JavaScript files
│   └── *.html             # HTML pages
├── nginx/                 # Nginx configuration
├── alembic.ini            # Alembic configuration
├── docker-compose.yml     # Docker Compose configuration
├── docker-compose.override.yml # Docker Compose overrides
├── start.sh               # Production startup script
├── start.bat              # Windows startup script
└── .env.example           # Environment variables template
```

## 🔧 Configuration

### Environment Variables

Key environment variables to configure:

- `DATABASE_URL` - Database connection string
- `SECRET_KEY` - JWT secret key (must be secure in production)
- `REDIS_HOST` - Redis server host (optional)
- `SMTP_*` - Email configuration for OTP delivery
- `ALLOWED_ORIGINS` - CORS allowed origins

### Database Migration

```bash
# Create new migration
alembic revision --autogenerate -m "description"

# Apply migrations
alembic upgrade head

# Rollback migration
alembic downgrade -1
```

## 🔒 Security

- All passwords are hashed using bcrypt
- JWT tokens for authentication
- Email OTP verification for signup
- WebSocket connections require authentication
- CORS configured for allowed origins
- Input validation on all endpoints

## 🧪 Testing

```bash
# Run backend tests
cd backend
pytest

# Run with coverage
pytest --cov=app tests/
```

## 📦 Deployment

### Using Docker Compose

```bash
docker-compose up -d
```

### Manual Deployment

1. Set up a production server (Ubuntu/Debian recommended)
2. Install Python 3.8+ and dependencies
3. Configure Nginx as reverse proxy
4. Set up SSL/TLS certificates (Let's Encrypt)
5. Use a process manager (systemd, supervisor)
6. Configure firewall (allow ports 80, 443, 8000)

### Environment Setup

```bash
# Production settings
DEBUG=False
SECRET_KEY=<generate-strong-random-key>
ALLOWED_ORIGINS=https://yourdomain.com
```

## 🌟 API Endpoints

### Authentication
- `POST /api/auth/register` - Register new user
- `POST /api/auth/verify-otp` - Verify email OTP
- `POST /api/auth/login` - User login
- `GET /api/auth/me` - Get current user

### Rooms
- `GET /api/rooms/` - List all rooms
- `POST /api/rooms/` - Create new room
- `GET /api/rooms/{room_id}` - Get room details
- `POST /api/rooms/{room_id}/join` - Join a room
- `POST /api/rooms/{room_id}/leave` - Leave a room

### WebSocket
- `WS /ws/signaling/{room_id}` - WebRTC signaling

## 🛡️ Production Checklist

- [ ] Change `SECRET_KEY` to a secure random string
- [ ] Set `DEBUG=False`
- [ ] Configure proper CORS origins
- [ ] Set up SSL/TLS certificates
- [ ] Configure email SMTP settings
- [ ] Set up database backups
- [ ] Configure logging
- [ ] Set up monitoring (optional)
- [ ] Configure Redis for production (optional)
- [ ] Use PostgreSQL instead of SQLite (recommended)

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## 📄 License

This project is licensed under the MIT License.

## 🆘 Support

For issues and questions:
- Open an issue on GitHub
- Check the API documentation at `/docs`

## 🎯 Tech Stack

**Backend:**
- FastAPI (Python web framework)
- SQLAlchemy (ORM)
- PostgreSQL (Database)
- JWT (Authentication)
- WebSocket (Real-time signaling)
- Redis (Optional caching)

**Frontend:**
- Vanilla JavaScript
- HTML5
- CSS3 (Premium dark theme)
- WebRTC API

**DevOps:**
- Docker & Docker Compose
- Nginx (Reverse proxy)
- Alembic (Database migrations)

---

Built with ❤️ using FastAPI and WebRTC

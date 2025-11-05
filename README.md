# WebRTC Video/Audio Communication App

A complete, production-ready backend for real-time video/audio communication using WebRTC, FastAPI, PostgreSQL, and WebSockets.

## 🚀 Features

- **User Authentication**: JWT-based authentication with email verification
- **WebRTC Signaling Server**: Custom WebSocket-based signaling for SDP offer/answer and ICE candidate exchange
- **Multi-room Support**: Multiple rooms with multiple users per room
- **Database Integration**: PostgreSQL with SQLAlchemy ORM and Alembic migrations
- **REST API**: Full API for user management, room creation, and health checks
- **Dockerized Setup**: Ready-to-deploy Docker configuration with PostgreSQL and Redis
- **Security**: CORS setup, HTTPS-ready configuration
- **Monitoring**: Prometheus metrics endpoint
- **Frontend**: Simple HTML/JavaScript client for testing

## 🛠️ Tech Stack

- **Python 3.11+**
- **FastAPI** - High performance web framework
- **PostgreSQL** - Relational database
- **SQLAlchemy** - ORM for database operations
- **Alembic** - Database migration tool
- **WebSockets** - Real-time communication
- **Redis** - Optional for session storage
- **Docker** - Containerization
- **Nginx** - Reverse proxy
- **Prometheus** - Metrics collection
- **Pydantic** - Data validation
- **Pytest** - Testing framework

## 📁 Project Structure

```
webRTC/
├── backend/
│   ├── alembic/           # Database migrations
│   ├── app/
│   │   ├── api/           # REST API routes
│   │   ├── core/          # Configuration and database setup
│   │   ├── models/        # Database models and Pydantic schemas
│   │   ├── schemas/       # Request/response schemas
│   │   ├── signaling/     # WebSocket signaling server
│   │   ├── utils/         # Utility functions
│   │   └── main.py        # Application entry point
│   ├── Dockerfile         # Backend Docker configuration
│   ├── requirements.txt   # Python dependencies
│   └── .env              # Environment variables
├── frontend/              # Simple HTML/JS client
├── nginx/                 # Nginx configuration
├── docker-compose.yml     # Docker Compose setup
└── README.md             # This file
```

## 🚀 Quick Start

### Prerequisites

- Docker and Docker Compose
- Python 3.11+ (for local development)

### Using Docker (Recommended)

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd webRTC
   ```

2. **Start the application:**
   ```bash
   docker-compose up -d
   ```

3. **Access the services:**
   - API Documentation: http://localhost:8000/docs
   - Frontend: http://localhost
   - Metrics: http://localhost:8000/api/metrics

### Local Development

1. **Install dependencies:**
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

2. **Set up the database:**
   ```bash
   # Start PostgreSQL (using Docker)
   docker-compose up -d db
   
   # Run database migrations
   alembic upgrade head
   ```

3. **Start the server:**
   ```bash
   python app/main.py
   ```

4. **Access the application:**
   - API: http://localhost:8000
   - WebSocket: ws://localhost:8000/ws/signaling

## 🗃️ Database Schema

### Users Table
- `id`: Integer (Primary Key)
- `email`: String (Unique)
- `is_verified`: Boolean
- `username`: String (Unique)
- `hashed_password`: String
- `created_at`: DateTime

### OTPs Table
- `id`: Integer (Primary Key)
- `email`: String
- `otp`: String
- `expiry`: DateTime
- `created_at`: DateTime

### Rooms Table
- `id`: Integer (Primary Key)
- `room_id`: String (Unique)
- `created_at`: DateTime
- `owner_id`: Integer (Foreign Key to Users)

### Room Participants (Association Table)
- `room_id`: Integer (Foreign Key to Rooms)
- `user_id`: Integer (Foreign Key to Users)

## 🔐 Authentication Flow

1. **Signup**: POST `/api/auth/signup`
   - Accepts email
   - Generates and stores OTP
   - Sends OTP to email
   - Stores user with `is_verified = False`

2. **Verify OTP**: POST `/api/auth/verify-otp`
   - Accepts email + OTP
   - Verifies OTP and sets `is_verified = True`

3. **Set Username**: POST `/api/auth/set-username`
   - Accepts email + desired username
   - Validates username (lowercase, alphanumeric, unique)
   - Stores username linked to email

4. **Login**: POST `/api/auth/login`
   - Accepts email
   - Returns JWT token if email is verified

## 📡 API Endpoints

### Authentication
- `POST /api/auth/signup` - Create new user account
- `POST /api/auth/verify-otp` - Verify email with OTP
- `POST /api/auth/set-username` - Set username for account
- `POST /api/auth/login` - Obtain access token

### Rooms
- `POST /api/rooms/` - Create new room
- `GET /api/rooms/` - List all rooms user is part of
- `GET /api/rooms/{room_id}` - Get room details
- `POST /api/rooms/{room_id}/join` - Join a room
- `POST /api/rooms/{room_id}/leave` - Leave a room

### System
- `GET /health` - Health check
- `GET /api/metrics` - Prometheus metrics

## 🌐 WebSocket Signaling

### Connection
Connect to: `ws://localhost:8000/ws/signaling/{room_id}`

Authentication is handled via JWT token in the Authorization header.

### Message Types

1. **Offer**
   ```json
   {
     "type": "offer",
     "sdp": "offer SDP string",
     "target": "recipient_username"
   }
   ```

2. **Answer**
   ```json
   {
     "type": "answer",
     "sdp": "answer SDP string",
     "target": "recipient_username"
   }
   ```

3. **ICE Candidate**
   ```json
   {
     "type": "candidate",
     "candidate": { /* ICE candidate object */ },
     "target": "recipient_username"
   }
   ```

4. **User Joined**
   ```json
   {
     "type": "user_joined",
     "username": "username",
     "room_id": "room_id"
   }
   ```

5. **User Left**
   ```json
   {
     "type": "user_left",
     "username": "username",
     "room_id": "room_id"
   }
   ```

## 🔐 Environment Variables

Create a `.env` file in the backend directory:

```env
# Application settings
PROJECT_NAME=WebRTC Communication App
DEBUG=False
VERSION=1.0.0

# Server settings
HOST=0.0.0.0
PORT=8000

# Security settings
SECRET_KEY=your-super-secret-key-here-change-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# CORS settings
BACKEND_CORS_ORIGINS=["*"]

# Database settings
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/webrtc_db

# Redis settings
REDIS_URL=redis://localhost:6379

# Email settings (for OTP)
SMTP_SERVER=localhost
SMTP_PORT=1025
EMAIL_USER=test@example.com
EMAIL_PASSWORD=password
```

## 🚢 Deployment

### Railway/Render Deployment

1. Set environment variables in your deployment platform
2. Deploy the backend directory as a web service
3. Add PostgreSQL and Redis as separate services

### VPS Deployment

1. Install Docker and Docker Compose on your VPS
2. Clone the repository
3. Update the `docker-compose.yml` with your domain/IP
4. Run `docker-compose up -d`

### HTTPS Setup

For production deployments, update the Nginx configuration to include SSL certificates.

## 🧪 Testing

Run the test suite:

```bash
cd backend
pytest
```

## 📊 Monitoring

The application exposes Prometheus metrics at `/api/metrics` endpoint.

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Open a pull request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

For support, please open an issue on the repository.
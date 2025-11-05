# WebRTC Communication App - Frontend

A complete frontend implementation for a WebRTC-based video/audio communication application built with pure HTML, CSS, and Vanilla JavaScript.

## Features

✅ **Pure HTML/CSS/JavaScript** - No build tools, no npm, no dependencies
✅ **Responsive Design** - Mobile-first layout with Flexbox/Grid
✅ **Full Authentication Flow** - Email signup, OTP verification, login
✅ **Room Management** - Create, join, list, and leave rooms
✅ **WebRTC Video/Audio** - Real-time peer-to-peer communication
✅ **WebSocket Signaling** - Live connection management
✅ **Modern UI** - Clean, minimal design with smooth animations

## File Structure

```
frontend/
├── index.html          # Landing page
├── signup.html         # User registration
├── verify.html         # OTP verification
├── username.html       # Username display after verification
├── login.html          # Login page
├── dashboard.html      # Room management dashboard
├── room.html           # Video chat room
├── 404.html            # Error page
├── js/
│   ├── auth.js         # Authentication logic
│   ├── rooms.js        # Room API operations
│   ├── dashboard.js    # Dashboard UI logic
│   ├── signaling.js    # WebSocket signaling
│   └── webrtc.js       # WebRTC peer connections
└── css/
    └── styles.css      # Responsive styling
```

## Navigation Flow

```
index.html
  ├─> signup.html
  │     └─> verify.html
  │           └─> username.html
  │                 └─> login.html
  └─> login.html
        └─> dashboard.html
              └─> room.html
```

## API Endpoints Used

### Authentication
- `POST /api/auth/register` - Register with email + password
- `POST /api/auth/verify-otp` - Verify OTP code
- `POST /api/auth/login` - Login with username + password

### Rooms
- `GET /api/rooms/` - List all available rooms
- `POST /api/rooms/` - Create a new room
- `POST /api/rooms/{room_id}/join` - Join a room
- `POST /api/rooms/{room_id}/leave` - Leave a room

### WebSocket
- `ws://localhost:8000/ws/signaling/{room_id}` - Signaling server

## WebSocket Message Types

- `offer` - WebRTC offer from peer
- `answer` - WebRTC answer to offer
- `candidate` - ICE candidate exchange
- `user_joined` - Notification when user joins
- `user_left` - Notification when user leaves
- `heartbeat` - Keep connection alive

## Local Storage Usage

- `authToken` - JWT authentication token
- `assignedUsername` - User's username
- `pendingEmail` - Email during signup flow
- `pendingPassword` - Password during signup flow

## Responsive Breakpoints

- **Mobile**: ≤600px (stacked layout)
- **Tablet**: 600-1024px (two-column layout)
- **Desktop**: >1024px (full-width layout)

## How to Run

1. Start the backend server:
   ```bash
   cd backend
   python -m app.main
   ```

2. Open browser and navigate to:
   ```
   http://localhost:8000/
   ```

3. The frontend is served directly by FastAPI at:
   - `/` - Landing page
   - `/signup` - Signup page
   - `/login` - Login page
   - `/dashboard` - Dashboard
   - `/room` - Video room

## Browser Requirements

- WebRTC support (Chrome 70+, Firefox 60+, Safari 12+)
- WebSocket support
- getUserMedia API (camera/microphone access)
- Modern ES6+ JavaScript support

## Security Features

- JWT-based authentication
- Token stored in localStorage
- Protected routes (redirect to login if not authenticated)
- HTTPS recommended for production

## Development Notes

- All JavaScript is vanilla ES6+
- No transpilation required
- CSS uses CSS Grid and Flexbox
- Mobile-first responsive design
- Cross-browser compatible

## Troubleshooting

### Camera/Microphone Access
- Ensure HTTPS (or localhost) for getUserMedia
- Check browser permissions
- Test in supported browsers

### WebSocket Connection
- Verify backend is running on port 8000
- Check CORS settings
- Ensure firewall allows WebSocket connections

### Authentication Issues
- Clear localStorage and try again
- Check JWT token expiration
- Verify backend API is accessible

## Future Enhancements

- Screen sharing support
- Chat messaging
- File sharing
- Recording functionality
- Multiple video layouts
- Virtual backgrounds

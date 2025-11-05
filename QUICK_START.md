# Quick Start Guide - WebRTC Communication App

## Getting Started

The WebRTC Communication App is now running! Follow these steps to test all features.

## 🚀 Access the Application

The application is now running at: **http://localhost:8000**

Click the preview button to open the application in your browser.

## 📋 Testing Checklist

### 1. Landing Page
- ✅ Visit http://localhost:8000/
- ✅ Click "Get Started" → should go to signup page
- ✅ Click "Sign In" → should go to login page

### 2. User Registration Flow

**Step 1: Sign Up**
- Navigate to http://localhost:8000/signup
- Enter email: `test@example.com`
- Enter password: `password123`
- Confirm password: `password123`
- Click "Sign Up"

**Step 2: Verify OTP**
- Check the backend console for the OTP code (it will be printed there in development mode)
- Enter the 6-digit OTP code
- Click "Verify Email"

**Step 3: View Username**
- Your auto-generated username will be displayed
- Click "Continue to Login"

### 3. Login

**Login with Generated Username**
- Enter your username (from previous step)
- Enter password: `password123`
- Click "Sign In"
- You should be redirected to the dashboard

### 4. Dashboard & Room Management

**Create a Room**
- Click "+ Create Room" button
- Enter room name: "Test Room"
- Click "Create"
- The room should appear in the list

**Join a Room**
- Click "Join Room" on any available room
- You should be redirected to the video chat room

### 5. Video Chat Room

**In the Room:**
- Allow camera and microphone access when prompted
- Your video should appear in the local video container
- Test the controls:
  - 🎤 Toggle audio on/off
  - 📹 Toggle video on/off
  - 📞 End call (returns to dashboard)
- Click "Leave Room" to exit

### 6. Multi-User Testing

To test real WebRTC communication:

**In Browser 1:**
1. Sign up as user1@example.com
2. Login with generated username
3. Create a room called "Meeting Room"
4. Join the room

**In Browser 2 (Incognito/Private Window):**
1. Sign up as user2@example.com
2. Login with generated username
3. You should see "Meeting Room" in the list
4. Join the same room
5. Both users should see each other's video!

## 🔍 API Testing

### Check API Documentation
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

### Test API Endpoints

**Health Check:**
```bash
curl http://localhost:8000/health
```

**Register User:**
```bash
curl -X POST http://localhost:8000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"api@test.com","password":"test1234"}'
```

**List Rooms:**
```bash
curl http://localhost:8000/api/rooms/ \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

## 🐛 Troubleshooting

### Camera/Microphone Not Working
- Ensure you're using HTTPS or localhost
- Check browser permissions
- Try a different browser (Chrome/Firefox recommended)

### OTP Not Received
- Check the backend console - OTP is printed there in development mode
- Format: `Development mode: OTP for email@example.com is: 123456`

### WebSocket Connection Failed
- Ensure backend is running on port 8000
- Check browser console for errors
- Verify WebSocket URL: `ws://localhost:8000/ws/signaling/{room_id}`

### Login Not Working
- Make sure you verified your email with OTP first
- Use the auto-generated username (shown after OTP verification)
- Check localStorage in browser dev tools

### No Rooms Showing
- Create a room first
- Refresh the dashboard
- Check browser console for API errors

## 📝 Development Notes

### View Backend Logs
The backend console will show:
- OTP codes (in development mode)
- API requests
- WebSocket connections
- Database operations

### Browser Developer Tools
Press F12 to open:
- **Console**: View JavaScript logs and errors
- **Network**: Monitor API calls and WebSocket traffic
- **Application > Local Storage**: View stored JWT tokens

### File Locations
- Frontend: `d:\Virtual EnV\FastAPI\projects\webRTC\frontend\`
- Backend: `d:\Virtual EnV\FastAPI\projects\webRTC\backend\`
- Database: `d:\Virtual EnV\FastAPI\projects\webRTC\backend\test.db`

## 🎯 Key Features to Test

1. ✅ Responsive design (resize browser window)
2. ✅ Form validation (try invalid inputs)
3. ✅ Error handling (try wrong credentials)
4. ✅ Navigation flow (use browser back button)
5. ✅ Real-time updates (join room from multiple browsers)
6. ✅ WebRTC connection (video/audio streaming)
7. ✅ Control buttons (mute/unmute, camera on/off)

## 🔐 Test Credentials

You can create multiple test users:
- user1@test.com / password123
- user2@test.com / password123
- user3@test.com / password123

Each will get a unique auto-generated username after OTP verification.

## 📱 Mobile Testing

To test on mobile devices on your local network:
1. Find your computer's IP address
2. Access: `http://YOUR_IP:8000`
3. Note: Camera/mic access requires HTTPS (except localhost)

## ✨ Next Steps

After testing the basic functionality:
1. Create multiple rooms
2. Test concurrent users in same room
3. Test ICE candidate exchange
4. Monitor WebRTC connection states
5. Test on different browsers
6. Test on different devices

## 🛑 Stopping the Server

To stop the backend server:
- Press `Ctrl+C` in the terminal
- Or close the terminal window

---

**Enjoy your WebRTC Communication App! 🎉**

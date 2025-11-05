# Frontend Testing Checklist

## ✅ Authentication Flow

### Signup Page (`/signup`)
- [ ] Email validation (requires valid email format)
- [ ] Password validation (minimum 8 characters)
- [ ] Password confirmation matching
- [ ] Show error messages for invalid inputs
- [ ] Successful signup redirects to `/verify`
- [ ] "Already have an account?" link goes to `/login`

### Verify OTP Page (`/verify`)
- [ ] Email address is displayed correctly
- [ ] OTP input accepts only 6 digits
- [ ] Successful verification redirects to `/username`
- [ ] "Resend OTP" link works
- [ ] Error shown for invalid OTP
- [ ] Error shown for expired OTP
- [ ] "Back to Sign Up" link works
- [ ] Redirects to `/signup` if no pending email

### Username Display Page (`/username`)
- [ ] Auto-generated username is displayed
- [ ] "Continue to Login" button works
- [ ] Redirects to `/signup` if no username found

### Login Page (`/login`)
- [ ] Username field validation
- [ ] Password field validation
- [ ] Successful login redirects to `/dashboard`
- [ ] Error shown for invalid credentials
- [ ] "Don't have an account?" link goes to `/signup`
- [ ] Already logged-in users redirect to `/dashboard`

## ✅ Dashboard Page (`/dashboard`)

### UI Elements
- [ ] Username displayed in navbar
- [ ] Logout button works
- [ ] "+ Create Room" button shows create form
- [ ] Rooms grid displays correctly
- [ ] Empty state shown when no rooms

### Room Management
- [ ] Create room with valid name
- [ ] Cancel create room hides form
- [ ] Room cards show correct information
- [ ] Join room button works
- [ ] Joining redirects to `/room?room_id=xxx`
- [ ] Rooms auto-refresh every 10 seconds

### Responsive Design
- [ ] Mobile (≤600px): stacked layout
- [ ] Tablet (600-1024px): 2-column grid
- [ ] Desktop (>1024px): 3-column grid

## ✅ Video Chat Room (`/room`)

### Initial Setup
- [ ] Room ID shown in navbar
- [ ] Camera/mic permission requested
- [ ] Local video stream displayed
- [ ] "You" label on local video
- [ ] Connection status shown

### Video Controls
- [ ] Toggle audio button works (🎤/🔇)
- [ ] Toggle video button works (📹/📵)
- [ ] End call button returns to dashboard
- [ ] Leave room button returns to dashboard

### WebRTC Features
- [ ] Remote videos appear when peers join
- [ ] Remote video labels show usernames
- [ ] Videos removed when peers leave
- [ ] ICE candidates exchanged
- [ ] Offer/answer flow works
- [ ] Heartbeat keeps connection alive

### Error Handling
- [ ] Invalid room ID redirects to dashboard
- [ ] Missing username redirects to login
- [ ] Camera/mic denied shows error
- [ ] Connection lost shows error
- [ ] Page unload stops media streams

## ✅ Landing Page (`/`)

- [ ] Page loads correctly
- [ ] Feature cards displayed
- [ ] "Get Started" button goes to `/signup`
- [ ] "Sign In" button goes to `/login`
- [ ] Responsive layout works

## ✅ Error Page (`/404`)

- [ ] 404 icon displayed
- [ ] "Go Home" button works
- [ ] "Go Back" button works
- [ ] Page styling matches theme

## ✅ Cross-Browser Testing

### Chrome
- [ ] All pages load
- [ ] WebRTC works
- [ ] WebSocket works
- [ ] Camera/mic access works

### Firefox
- [ ] All pages load
- [ ] WebRTC works
- [ ] WebSocket works
- [ ] Camera/mic access works

### Safari
- [ ] All pages load
- [ ] WebRTC works
- [ ] WebSocket works
- [ ] Camera/mic access works

### Edge
- [ ] All pages load
- [ ] WebRTC works
- [ ] WebSocket works
- [ ] Camera/mic access works

## ✅ Mobile Testing

### Mobile Chrome
- [ ] Responsive layout
- [ ] Touch interactions work
- [ ] Camera switch (front/back)
- [ ] Video orientation correct

### Mobile Safari
- [ ] Responsive layout
- [ ] Touch interactions work
- [ ] Camera switch (front/back)
- [ ] Video orientation correct

## ✅ Security Testing

- [ ] JWT stored in localStorage
- [ ] Token attached to authenticated requests
- [ ] Unauthenticated users redirected to login
- [ ] Token expiration handled
- [ ] XSS prevention (HTML escaping)
- [ ] CORS headers configured

## ✅ Performance Testing

- [ ] Page load time < 2 seconds
- [ ] Video latency < 500ms
- [ ] WebSocket reconnection works
- [ ] Multiple peers (3+) work smoothly
- [ ] Memory usage reasonable
- [ ] No memory leaks after leaving room

## ✅ UI/UX Testing

### Visual Design
- [ ] Consistent color scheme
- [ ] Readable fonts
- [ ] Proper spacing
- [ ] Button hover states
- [ ] Loading indicators
- [ ] Success/error messages styled

### Interactions
- [ ] Form submission feedback
- [ ] Button disabled states
- [ ] Input focus states
- [ ] Smooth transitions
- [ ] No layout shifts
- [ ] Keyboard navigation works

### Responsive Behavior
- [ ] No horizontal scroll
- [ ] Text readable on small screens
- [ ] Buttons easily tappable (44px+)
- [ ] Forms usable on mobile
- [ ] Videos scale properly

## ✅ Accessibility Testing

- [ ] Semantic HTML used
- [ ] Form labels present
- [ ] Alt text for icons
- [ ] Keyboard accessible
- [ ] Focus indicators visible
- [ ] Color contrast sufficient

## ✅ Edge Cases

- [ ] Very long room names
- [ ] Special characters in input
- [ ] Slow network connection
- [ ] Network disconnection/reconnection
- [ ] Browser refresh during video call
- [ ] Multiple tabs open
- [ ] Back button navigation

## ✅ API Integration

- [ ] Correct endpoints called
- [ ] Request headers correct
- [ ] Request body formatted correctly
- [ ] Response errors handled
- [ ] Network errors handled
- [ ] Loading states shown

## ✅ LocalStorage Testing

- [ ] Token persists after refresh
- [ ] Username persists after refresh
- [ ] Pending email cleared after verification
- [ ] Data cleared on logout

## ✅ WebSocket Testing

- [ ] Connection established
- [ ] Messages sent correctly
- [ ] Messages received correctly
- [ ] Reconnection on disconnect
- [ ] Heartbeat sent every 30s
- [ ] Connection closed on page unload

## 📊 Test Results Summary

**Date:** _____________

**Tester:** _____________

**Browser/Device:** _____________

**Pass Rate:** _____ / _____ (____%)

**Critical Issues:** _____________

**Notes:** _____________

---

## 🐛 Bug Report Template

**Title:** _____________

**Severity:** [ ] Critical [ ] High [ ] Medium [ ] Low

**Steps to Reproduce:**
1. _____________
2. _____________
3. _____________

**Expected Result:** _____________

**Actual Result:** _____________

**Browser/Device:** _____________

**Screenshots:** _____________

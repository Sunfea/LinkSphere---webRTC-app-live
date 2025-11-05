// WebRTC Room Logic
// Handles WebRTC peer connections and media streams

// Check authentication
if (!requireAuth()) {
    throw new Error('Authentication required');
}

// ========================
// Configuration
// ========================

const ICE_SERVERS = {
    iceServers: [
        { urls: 'stun:stun.l.google.com:19302' },
        { urls: 'stun:stun1.l.google.com:19302' }
    ]
};

// ========================
// Global State
// ========================

let roomId = null;
let username = null;
let signalingClient = null;
let localStream = null;
let peerConnections = {};
let isAudioEnabled = true;
let isVideoEnabled = true;

// ========================
// Initialization
// ========================

async function initRoom() {
    // Get room ID from URL
    const params = new URLSearchParams(window.location.search);
    roomId = params.get('room_id');
    
    if (!roomId) {
        showStatus('Invalid room ID', true);
        setTimeout(() => window.location.href = '/dashboard', 2000);
        return;
    }
    
    // Get username
    username = getUsernameFromToken() || localStorage.getItem('assignedUsername');
    
    if (!username) {
        showStatus('Username not found', true);
        setTimeout(() => window.location.href = '/login', 2000);
        return;
    }
    
    // Update UI
    document.getElementById('roomId').textContent = `ID: ${roomId}`;
    
    try {
        // Get local media
        showStatus('Requesting camera and microphone access...');
        await setupLocalMedia();
        
        // Connect to signaling server
        showStatus('Connecting to room...');
        await setupSignaling();
        
        showStatus('Connected to room');
        
    } catch (error) {
        console.error('Failed to initialize room:', error);
        showStatus(`Error: ${error.message}`, true);
    }
}

// ========================
// Media Setup
// ========================

async function setupLocalMedia() {
    try {
        localStream = await navigator.mediaDevices.getUserMedia({
            video: {
                width: { ideal: 1280 },
                height: { ideal: 720 }
            },
            audio: {
                echoCancellation: true,
                noiseSuppression: true
            }
        });
        
        const localVideo = document.getElementById('localVideo');
        localVideo.srcObject = localStream;
        
        console.log('Local media stream obtained');
        
    } catch (error) {
        console.error('Failed to get local media:', error);
        throw new Error('Camera/microphone access denied. Please allow access and refresh.');
    }
}

// ========================
// Signaling Setup
// ========================

async function setupSignaling() {
    signalingClient = new SignalingClient(roomId, username);
    
    // Register message handlers
    signalingClient.on('user_joined', handleUserJoined);
    signalingClient.on('user_left', handleUserLeft);
    signalingClient.on('offer', handleOffer);
    signalingClient.on('answer', handleAnswer);
    signalingClient.on('candidate', handleCandidate);
    signalingClient.on('connection_lost', handleConnectionLost);
    
    // Connect to WebSocket
    await signalingClient.connect();
}

// ========================
// Signaling Handlers
// ========================

async function handleUserJoined(message) {
    const peerUsername = message.username;
    
    if (peerUsername === username) {
        console.log('Self joined - ignoring');
        return;
    }
    
    console.log('User joined:', peerUsername);
    showStatus(`${peerUsername} joined the room`);
    
    // Create peer connection and send offer
    await createPeerConnection(peerUsername);
    await createAndSendOffer(peerUsername);
}

function handleUserLeft(message) {
    const peerUsername = message.username;
    
    console.log('User left:', peerUsername);
    showStatus(`${peerUsername} left the room`);
    
    // Close peer connection
    closePeerConnection(peerUsername);
    removeRemoteVideo(peerUsername);
}

async function handleOffer(message) {
    const peerUsername = message.from;
    const offer = message.sdp;
    
    console.log('Received offer from:', peerUsername);
    
    // Create peer connection if doesn't exist
    if (!peerConnections[peerUsername]) {
        await createPeerConnection(peerUsername);
    }
    
    const pc = peerConnections[peerUsername];
    
    try {
        await pc.setRemoteDescription(new RTCSessionDescription(offer));
        
        // Create and send answer
        const answer = await pc.createAnswer();
        await pc.setLocalDescription(answer);
        
        signalingClient.sendAnswer(peerUsername, answer);
        
    } catch (error) {
        console.error('Failed to handle offer:', error);
    }
}

async function handleAnswer(message) {
    const peerUsername = message.from;
    const answer = message.sdp;
    
    console.log('Received answer from:', peerUsername);
    
    const pc = peerConnections[peerUsername];
    
    if (pc) {
        try {
            await pc.setRemoteDescription(new RTCSessionDescription(answer));
        } catch (error) {
            console.error('Failed to handle answer:', error);
        }
    }
}

async function handleCandidate(message) {
    const peerUsername = message.from;
    const candidate = message.candidate;
    
    console.log('Received ICE candidate from:', peerUsername);
    
    const pc = peerConnections[peerUsername];
    
    if (pc) {
        try {
            await pc.addIceCandidate(new RTCIceCandidate(candidate));
        } catch (error) {
            console.error('Failed to add ICE candidate:', error);
        }
    }
}

function handleConnectionLost() {
    showStatus('Connection lost. Please refresh the page.', true);
}

// ========================
// Peer Connection Management
// ========================

async function createPeerConnection(peerUsername) {
    console.log('Creating peer connection for:', peerUsername);
    
    const pc = new RTCPeerConnection(ICE_SERVERS);
    peerConnections[peerUsername] = pc;
    
    // Add local stream tracks
    localStream.getTracks().forEach(track => {
        pc.addTrack(track, localStream);
    });
    
    // Handle ICE candidates
    pc.onicecandidate = (event) => {
        if (event.candidate) {
            signalingClient.sendCandidate(peerUsername, event.candidate);
        }
    };
    
    // Handle remote stream
    pc.ontrack = (event) => {
        console.log('Received remote track from:', peerUsername);
        addRemoteVideo(peerUsername, event.streams[0]);
    };
    
    // Handle connection state
    pc.onconnectionstatechange = () => {
        console.log(`Connection state with ${peerUsername}:`, pc.connectionState);
        
        if (pc.connectionState === 'disconnected' || pc.connectionState === 'failed') {
            closePeerConnection(peerUsername);
            removeRemoteVideo(peerUsername);
        }
    };
    
    return pc;
}

async function createAndSendOffer(peerUsername) {
    const pc = peerConnections[peerUsername];
    
    if (!pc) return;
    
    try {
        const offer = await pc.createOffer();
        await pc.setLocalDescription(offer);
        
        signalingClient.sendOffer(peerUsername, offer);
        
    } catch (error) {
        console.error('Failed to create offer:', error);
    }
}

function closePeerConnection(peerUsername) {
    const pc = peerConnections[peerUsername];
    
    if (pc) {
        pc.close();
        delete peerConnections[peerUsername];
    }
}

// ========================
// Video UI Management
// ========================

function addRemoteVideo(peerUsername, stream) {
    // Check if video already exists
    let videoContainer = document.getElementById(`video-${peerUsername}`);
    
    if (!videoContainer) {
        videoContainer = document.createElement('div');
        videoContainer.id = `video-${peerUsername}`;
        videoContainer.className = 'video-container remote-video';
        
        const video = document.createElement('video');
        video.autoplay = true;
        video.playsInline = true;
        video.srcObject = stream;
        
        const label = document.createElement('div');
        label.className = 'video-label';
        label.textContent = peerUsername;
        
        videoContainer.appendChild(video);
        videoContainer.appendChild(label);
        
        document.getElementById('videoGrid').appendChild(videoContainer);
    } else {
        const video = videoContainer.querySelector('video');
        video.srcObject = stream;
    }
}

function removeRemoteVideo(peerUsername) {
    const videoContainer = document.getElementById(`video-${peerUsername}`);
    if (videoContainer) {
        videoContainer.remove();
    }
}

// ========================
// Controls
// ========================

function toggleAudio() {
    isAudioEnabled = !isAudioEnabled;
    
    localStream.getAudioTracks().forEach(track => {
        track.enabled = isAudioEnabled;
    });
    
    const btn = document.getElementById('toggleAudioBtn');
    btn.classList.toggle('muted', !isAudioEnabled);
    btn.querySelector('.control-icon').textContent = isAudioEnabled ? '🎤' : '🔇';
}

function toggleVideo() {
    isVideoEnabled = !isVideoEnabled;
    
    localStream.getVideoTracks().forEach(track => {
        track.enabled = isVideoEnabled;
    });
    
    const btn = document.getElementById('toggleVideoBtn');
    btn.classList.toggle('disabled', !isVideoEnabled);
    btn.querySelector('.control-icon').textContent = isVideoEnabled ? '📹' : '📵';
}

async function endCall() {
    // Stop local media
    if (localStream) {
        localStream.getTracks().forEach(track => track.stop());
    }
    
    // Close all peer connections
    Object.keys(peerConnections).forEach(peerUsername => {
        closePeerConnection(peerUsername);
    });
    
    // Disconnect signaling
    if (signalingClient) {
        signalingClient.disconnect();
    }
    
    // Leave room via API
    try {
        await leaveRoom(roomId);
    } catch (error) {
        console.error('Failed to leave room:', error);
    }
    
    // Return to dashboard
    window.location.href = '/dashboard';
}

// ========================
// Event Listeners
// ========================

document.getElementById('toggleAudioBtn').addEventListener('click', toggleAudio);
document.getElementById('toggleVideoBtn').addEventListener('click', toggleVideo);
document.getElementById('endCallBtn').addEventListener('click', endCall);
document.getElementById('leaveRoomBtn').addEventListener('click', endCall);

// Handle page unload
window.addEventListener('beforeunload', () => {
    if (localStream) {
        localStream.getTracks().forEach(track => track.stop());
    }
    if (signalingClient) {
        signalingClient.disconnect();
    }
});

// ========================
// Utility Functions
// ========================

function showStatus(message, isError = false) {
    const statusElement = document.getElementById('roomStatus');
    statusElement.textContent = message;
    statusElement.className = `room-status ${isError ? 'error' : ''}`;
    
    // Auto-hide success messages after 3 seconds
    if (!isError) {
        setTimeout(() => {
            statusElement.textContent = '';
        }, 3000);
    }
}

// ========================
// Initialize on Load
// ========================

initRoom();

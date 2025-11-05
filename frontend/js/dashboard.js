// Dashboard Logic
// Handles room management UI

// Check authentication on page load
if (!requireAuth()) {
    throw new Error('Authentication required');
}

// Display username
const username = getUsernameFromToken() || localStorage.getItem('assignedUsername');
if (username) {
    document.getElementById('userDisplay').textContent = username;
}

// ========================
// UI State
// ========================

let currentRooms = [];

// ========================
// Event Listeners
// ========================

document.getElementById('logoutBtn').addEventListener('click', handleLogout);

document.getElementById('createRoomBtn').addEventListener('click', () => {
    document.getElementById('createRoomSection').style.display = 'block';
    document.getElementById('roomName').focus();
});

document.getElementById('cancelCreateBtn').addEventListener('click', () => {
    document.getElementById('createRoomSection').style.display = 'none';
    document.getElementById('createRoomForm').reset();
    clearMessage('createRoomMessage');
});

document.getElementById('createRoomForm').addEventListener('submit', handleCreateRoom);

// ========================
// Room Management Functions
// ========================

async function loadRooms() {
    const roomsGrid = document.getElementById('roomsGrid');
    
    try {
        roomsGrid.innerHTML = '<div class="loading">Loading rooms...</div>';
        
        const rooms = await window.listRooms();
        currentRooms = rooms;
        
        if (rooms.length === 0) {
            roomsGrid.innerHTML = '<div class="empty-state">No rooms available. Create one to get started!</div>';
            return;
        }
        
        roomsGrid.innerHTML = '';
        
        rooms.forEach(room => {
            const roomCard = createRoomCard(room);
            roomsGrid.appendChild(roomCard);
        });
        
    } catch (error) {
        console.error('Failed to load rooms:', error);
        roomsGrid.innerHTML = '<div class="error-state">Failed to load rooms. Please try again.</div>';
        showMessage('roomsMessage', error.message || 'Failed to load rooms', true);
    }
}

function createRoomCard(room) {
    const card = document.createElement('div');
    card.className = 'room-card';
    
    const participantCount = room.participants ? room.participants.length : 0;
    const isActive = participantCount > 0;
    
    card.innerHTML = `
        <span class="room-status-badge ${isActive ? 'active' : 'inactive'}">
            ${participantCount}
        </span>
        <div class="room-card-header">
            <h3 class="room-card-title">${escapeHtml(room.name)}</h3>
        </div>
        <div class="room-card-body">
            <div class="room-info">
                <span class="room-id" title="${room.room_id}">ID: ${room.room_id}</span>
            </div>
        </div>
        <div class="room-card-footer">
            <button class="btn btn-primary btn-small" onclick="handleJoinRoom('${room.room_id}')">
                🚀 Join
            </button>
            <button class="btn btn-secondary btn-small" onclick="handleInvite('${room.room_id}')">
                🔗 Invite
            </button>
        </div>
    `;
    
    return card;
}

async function handleCreateRoom(event) {
    event.preventDefault();
    
    const roomName = document.getElementById('roomName').value.trim();
    
    clearMessage('createRoomMessage');
    
    if (!roomName) {
        showMessage('createRoomMessage', 'Please enter a room name', true);
        return;
    }
    
    try {
        const room = await window.createRoom(roomName);
        
        showMessage('createRoomMessage', 'Room created successfully!', false);
        
        // Reset form and hide section
        document.getElementById('createRoomForm').reset();
        
        setTimeout(() => {
            document.getElementById('createRoomSection').style.display = 'none';
            clearMessage('createRoomMessage');
            loadRooms(); // Reload rooms list
        }, 1500);
        
    } catch (error) {
        showMessage('createRoomMessage', error.message || 'Failed to create room', true);
    }
}

async function handleJoinRoom(roomId) {
    try {
        await window.joinRoom(roomId);
        
        // Navigate to room page
        window.location.href = `/room?room_id=${roomId}`;
        
    } catch (error) {
        console.error('Failed to join room:', error);
        showMessage('roomsMessage', error.message || 'Failed to join room', true);
    }
}

function handleInvite(roomId) {
    const inviteLink = `${window.location.origin}/room?room_id=${roomId}`;
    
    // Copy to clipboard
    navigator.clipboard.writeText(inviteLink).then(() => {
        showMessage('roomsMessage', '✅ Invite link copied to clipboard!', false);
        setTimeout(() => clearMessage('roomsMessage'), 3000);
    }).catch(err => {
        // Fallback for older browsers
        const tempInput = document.createElement('input');
        tempInput.value = inviteLink;
        document.body.appendChild(tempInput);
        tempInput.select();
        document.execCommand('copy');
        document.body.removeChild(tempInput);
        showMessage('roomsMessage', '✅ Invite link copied to clipboard!', false);
        setTimeout(() => clearMessage('roomsMessage'), 3000);
    });
}

// Make functions globally accessible for inline onclick
window.handleJoinRoom = handleJoinRoom;
window.handleInvite = handleInvite;

// ========================
// Utility Functions
// ========================

function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

// ========================
// Initialize
// ========================

// With defer attribute, scripts execute in order after DOM is ready
console.log('Dashboard initializing...');
console.log('window.createRoom:', typeof window.createRoom);
console.log('window.listRooms:', typeof window.listRooms);
console.log('window.joinRoom:', typeof window.joinRoom);

// Load rooms immediately
loadRooms();

// Refresh rooms every 10 seconds
setInterval(loadRooms, 10000);

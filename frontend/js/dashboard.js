// Dashboard Logic
// Handles room management UI

console.log('📍 Dashboard.js: Script started executing');

// Room API Functions are now in rooms.js module

// Check authentication on page load
if (!requireAuth()) {
    throw new Error('Authentication required');
}

// ========================
// UI State
// ========================

let currentRooms = [];

// ========================
// Event Listeners
// ========================

// ========================
// Room Management Functions
// ========================

async function loadRooms() {
    const roomsGrid = document.getElementById('roomsGrid');
    console.log('loadRooms called');
    
    try {
        roomsGrid.innerHTML = '<div class="loading">Loading rooms...</div>';
        
        const rooms = await window.listRooms();
        console.log('Rooms loaded:', rooms);
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

// Function to manually load rooms module if it fails to load
function loadRoomsModuleManually() {
    console.log('Attempting to manually load rooms module...');
    
    // Check if rooms.js script is already in the document
    const existingScript = document.querySelector('script[src*="rooms.js"]');
    if (existingScript) {
        console.log('Rooms.js script already exists in document');
        if (existingScript.dataset.loaded) {
            console.log('Rooms.js script already loaded');
            return;
        }
        
        // Try to reload the script
        existingScript.remove();
    }
    
    // Create a new script element
    const script = document.createElement('script');
    script.src = '/static/js/rooms.js?v=14';
    script.dataset.loaded = 'false';
    
    script.onload = function() {
        console.log('Rooms.js script manually loaded');
        script.dataset.loaded = 'true';
        // Try to initialize dashboard again
        setTimeout(initializeDashboard, 100);
    };
    
    script.onerror = function(err) {
        console.error('Rooms.js script failed to load manually:', err);
        // Fallback: Define functions directly
        defineRoomFunctionsFallback();
    };
    
    document.head.appendChild(script);
}

// Fallback function definitions
function defineRoomFunctionsFallback() {
    console.log('Using fallback room functions...');
    
    if (typeof window.createRoom !== 'function') {
        window.createRoom = async function(roomName) {
            throw new Error('Room functions not available');
        };
    }
    
    if (typeof window.listRooms !== 'function') {
        window.listRooms = async function() {
            throw new Error('Room functions not available');
        };
    }
    
    if (typeof window.joinRoom !== 'function') {
        window.joinRoom = async function(roomId) {
            throw new Error('Room functions not available');
        };
    }
    
    // Try to initialize dashboard again
    setTimeout(initializeDashboard, 100);
}

// ========================
// Utility Functions
// ========================

function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

function showMessage(elementId, message, isError = false) {
    const element = document.getElementById(elementId);
    if (element) {
        element.textContent = message;
        element.className = `form-message ${isError ? 'error' : 'success'}`;
        element.style.display = 'block';
    }
}

function clearMessage(elementId) {
    const element = document.getElementById(elementId);
    if (element) {
        element.textContent = '';
        element.style.display = 'none';
    }
}

// ========================
// Initialize
// ========================

// With defer attribute, scripts execute in order after DOM is ready
console.log('Dashboard initializing...');
console.log('📍 Dashboard.js: Document ready state:', document.readyState);
console.log('📍 Dashboard.js: Current window object keys:', Object.keys(window).filter(key => key.includes('Room')));
console.log('window.createRoom:', typeof window.createRoom);
console.log('window.listRooms:', typeof window.listRooms);
console.log('window.joinRoom:', typeof window.joinRoom);

// Check if rooms.js script is actually loaded
console.log('Checking if rooms.js script is loaded...');
const roomsScript = document.querySelector('script[src*="rooms.js"]');
if (roomsScript) {
    console.log('Rooms.js script found in DOM');
    console.log('Rooms.js script src:', roomsScript.src);
    console.log('Rooms.js script readyState:', roomsScript.readyState);
} else {
    console.error('Rooms.js script not found in DOM');
}

// Wait for rooms module to be ready if not already loaded
function initializeDashboard(attempts = 0) {
    const maxAttempts = 100; // Increase max attempts
    
    console.log(`Checking for room functions (attempt ${attempts + 1}/${maxAttempts})...`);
    console.log('window.createRoom:', typeof window.createRoom);
    console.log('window.listRooms:', typeof window.listRooms);
    console.log('window.joinRoom:', typeof window.joinRoom);
    
    // Display username once DOM is ready
    displayUsername();
    
    // Add event listeners once DOM is ready
    const logoutBtn = document.getElementById('logoutBtn');
    const refreshRoomsBtn = document.getElementById('refreshRooms');
    const createRoomForm = document.getElementById('createRoomForm');
    
    if (logoutBtn) {
        logoutBtn.addEventListener('click', handleLogout);
    }
    
    if (refreshRoomsBtn) {
        refreshRoomsBtn.addEventListener('click', loadRooms);
    }
    
    if (createRoomForm) {
        createRoomForm.addEventListener('submit', handleCreateRoom);
    }
    
    if (typeof window.createRoom === 'function' && 
        typeof window.listRooms === 'function' && 
        typeof window.joinRoom === 'function') {
        console.log('All room functions found, loading rooms...');
        // Load rooms immediately
        loadRooms();
    } else {
        console.log('Rooms module not ready, waiting...');
        if (attempts < maxAttempts) {
            setTimeout(() => initializeDashboard(attempts + 1), 50); // Check more frequently
        } else {
            console.error('Maximum attempts reached, rooms module still not ready');
            // Try to manually load the rooms module
            loadRoomsModuleManually();
        }
    }
}

// Also listen for the custom event from rooms.js
window.addEventListener('roomsModuleLoaded', () => {
    console.log('Rooms module loaded event received');
    initializeDashboard();
});

// Add load and error event listeners to the rooms script
const roomsScriptElement = document.querySelector('script[src*="rooms.js"]');
if (roomsScriptElement) {
    roomsScriptElement.addEventListener('load', () => {
        console.log('Rooms.js script loaded successfully');
    });
    roomsScriptElement.addEventListener('error', (err) => {
        console.error('Rooms.js script failed to load:', err);
        // Try to manually load the rooms module
        loadRoomsModuleManually();
    });
}

initializeDashboard();

// Refresh rooms every 10 seconds
setInterval(loadRooms, 10000);

// Display username - moved to run after DOM is ready
function displayUsername() {
    const username = getUsernameFromToken() || localStorage.getItem('assignedUsername');
    const userDisplayElement = document.getElementById('userDisplay');
    if (username && userDisplayElement) {
        userDisplayElement.textContent = username;
    } else if (userDisplayElement) {
        userDisplayElement.textContent = 'Guest';
    }
}

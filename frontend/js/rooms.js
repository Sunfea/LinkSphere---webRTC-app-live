// Rooms API Module
// Handles all room-related API operations

console.log('🔄 Rooms.js: Script started loading');

// Immediately signal that this script is loading
window.roomsModuleLoading = true;
console.log('✅ Rooms.js: Set roomsModuleLoading = true');

const API_BASE_URL = 'http://localhost:8000';
console.log('✅ Rooms.js: API_BASE_URL set');

// ========================
// Room API Calls
// ========================

console.log('🔄 Rooms.js: Defining createRoom...');
window.createRoom = async function createRoom(roomName) {
    const token = localStorage.getItem('authToken');
    
    try {
        const response = await fetch(`${API_BASE_URL}/api/rooms/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            },
            body: JSON.stringify({ name: roomName })
        });
        
        const data = await response.json();
        
        if (!response.ok) {
            throw new Error(data.detail || 'Failed to create room');
        }
        
        return data;
    } catch (error) {
        console.error('Create room failed:', error);
        throw error;
    }
};

window.listRooms = async function listRooms() {
    const token = localStorage.getItem('authToken');
    
    try {
        const response = await fetch(`${API_BASE_URL}/api/rooms/`, {
            method: 'GET',
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });
        
        const data = await response.json();
        
        if (!response.ok) {
            throw new Error(data.detail || 'Failed to fetch rooms');
        }
        
        return data;
    } catch (error) {
        console.error('List rooms failed:', error);
        throw error;
    }
};

window.joinRoom = async function joinRoom(roomId) {
    const token = localStorage.getItem('authToken');
    
    try {
        const response = await fetch(`${API_BASE_URL}/api/rooms/${roomId}/join`, {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });
        
        const data = await response.json();
        
        if (!response.ok) {
            throw new Error(data.detail || 'Failed to join room');
        }
        
        return data;
    } catch (error) {
        console.error('Join room failed:', error);
        throw error;
    }
};

window.leaveRoom = async function leaveRoom(roomId) {
    const token = localStorage.getItem('authToken');
    
    try {
        const response = await fetch(`${API_BASE_URL}/api/rooms/${roomId}/leave`, {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });
        
        const data = await response.json();
        
        if (!response.ok) {
            throw new Error(data.detail || 'Failed to leave room');
        }
        
        return data;
    } catch (error) {
        console.error('Leave room failed:', error);
        throw error;
    }
};

window.getRoomDetails = async function getRoomDetails(roomId) {
    const token = localStorage.getItem('authToken');
    
    try {
        const response = await fetch(`${API_BASE_URL}/api/rooms/${roomId}`, {
            method: 'GET',
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });
        
        const data = await response.json();
        
        if (!response.ok) {
            throw new Error(data.detail || 'Failed to get room details');
        }
        
        return data;
    } catch (error) {
        console.error('Get room details failed:', error);
        throw error;
    }
};

// Log that rooms module is loaded
console.log('✅ Rooms.js: Module loaded successfully');

// Signal that rooms module is ready
window.roomsModuleReady = true;
console.log('✅ Rooms.js: Set roomsModuleReady = true');

// Trigger custom event
if (typeof Event !== 'undefined') {
    window.dispatchEvent(new Event('roomsModuleLoaded'));
    console.log('📢 Rooms.js: Dispatched roomsModuleLoaded event');
} else {
    console.warn('⚠️ Rooms.js: Event constructor not available');
}

console.log('🎯 Rooms.js: Initialization complete!');
console.log('Final check - window.createRoom:', typeof window.createRoom);
console.log('Final check - window.listRooms:', typeof window.listRooms);
console.log('Final check - window.joinRoom:', typeof window.joinRoom);

// WebSocket Signaling Module
// Handles WebSocket connection for WebRTC signaling

const WS_BASE_URL = '';

class SignalingClient {
    constructor(roomId, username) {
        this.roomId = roomId;
        this.username = username;
        this.ws = null;
        this.connected = false;
        this.messageHandlers = {};
        this.reconnectAttempts = 0;
        this.maxReconnectAttempts = 5;
        this.heartbeatInterval = null;
    }
    
    connect() {
        return new Promise((resolve, reject) => {
            try {
                // Get JWT token from localStorage
                const token = localStorage.getItem('authToken');
                if (!token) {
                    reject(new Error('No authentication token found'));
                    return;
                }
                
                // Include token in WebSocket URL as query parameter
                const wsUrl = `${WS_BASE_URL}/ws/signaling/${this.roomId}?token=${token}`;
                console.log('Connecting to signaling server...');
                
                this.ws = new WebSocket(wsUrl);
                
                this.ws.onopen = () => {
                    console.log('WebSocket connected');
                    this.connected = true;
                    this.reconnectAttempts = 0;
                    this.startHeartbeat();
                    resolve();
                };
                
                this.ws.onmessage = (event) => {
                    this.handleMessage(event.data);
                };
                
                this.ws.onerror = (error) => {
                    console.error('WebSocket error:', error);
                    reject(error);
                };
                
                this.ws.onclose = () => {
                    console.log('WebSocket disconnected');
                    this.connected = false;
                    this.stopHeartbeat();
                    this.handleDisconnect();
                };
                
            } catch (error) {
                console.error('Failed to create WebSocket:', error);
                reject(error);
            }
        });
    }
    
    handleMessage(data) {
        try {
            const message = JSON.parse(data);
            console.log('Received message:', message);
            
            const type = message.type;
            if (this.messageHandlers[type]) {
                this.messageHandlers[type](message);
            } else {
                console.warn('No handler for message type:', type);
            }
            
        } catch (error) {
            console.error('Failed to parse message:', error);
        }
    }
    
    on(messageType, handler) {
        this.messageHandlers[messageType] = handler;
    }
    
    send(message) {
        if (!this.connected || !this.ws) {
            console.error('Cannot send message: WebSocket not connected');
            return false;
        }
        
        try {
            const data = JSON.stringify({
                ...message,
                username: this.username
            });
            this.ws.send(data);
            console.log('Sent message:', message);
            return true;
        } catch (error) {
            console.error('Failed to send message:', error);
            return false;
        }
    }
    
    sendOffer(targetUsername, offer) {
        this.send({
            type: 'offer',
            target: targetUsername,
            sdp: offer
        });
    }
    
    sendAnswer(targetUsername, answer) {
        this.send({
            type: 'answer',
            target: targetUsername,
            sdp: answer
        });
    }
    
    sendCandidate(targetUsername, candidate) {
        this.send({
            type: 'candidate',
            target: targetUsername,
            candidate: candidate
        });
    }
    
    startHeartbeat() {
        this.heartbeatInterval = setInterval(() => {
            if (this.connected) {
                this.send({ type: 'heartbeat' });
            }
        }, 30000); // Every 30 seconds
    }
    
    stopHeartbeat() {
        if (this.heartbeatInterval) {
            clearInterval(this.heartbeatInterval);
            this.heartbeatInterval = null;
        }
    }
    
    handleDisconnect() {
        if (this.reconnectAttempts < this.maxReconnectAttempts) {
            this.reconnectAttempts++;
            console.log(`Attempting to reconnect (${this.reconnectAttempts}/${this.maxReconnectAttempts})...`);
            
            setTimeout(() => {
                this.connect().catch(error => {
                    console.error('Reconnect failed:', error);
                });
            }, 2000 * this.reconnectAttempts);
        } else {
            console.error('Max reconnect attempts reached');
            if (this.messageHandlers['connection_lost']) {
                this.messageHandlers['connection_lost']();
            }
        }
    }
    
    disconnect() {
        this.stopHeartbeat();
        if (this.ws) {
            this.ws.close();
            this.ws = null;
        }
        this.connected = false;
    }
}

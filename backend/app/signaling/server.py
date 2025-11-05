from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Depends, HTTPException, status
from typing import Dict
import json
import uuid
from app.signaling.manager import connection_manager
from app.core.auth_middleware import get_current_username_ws

# Create a separate FastAPI app for WebSocket signaling
signaling_app = FastAPI()

@signaling_app.websocket("/signaling/{room_id}")
async def websocket_endpoint(
    websocket: WebSocket, 
    room_id: str,
    username: str = Depends(get_current_username_ws)
):
    """
    WebSocket endpoint for WebRTC signaling
    Protected by JWT authentication
    Uses username instead of user_id for identification
    """
    # Connect the user to the room using username
    await connection_manager.connect(websocket, username, room_id)
    
    # Notify all users in the room that a new user joined
    await connection_manager.broadcast_to_room(room_id, {
        "type": "user_joined",
        "username": username,
        "room_id": room_id
    })
    
    try:
        while True:
            # Receive message from client
            data = await websocket.receive_text()
            message = json.loads(data)
            
            # Process different message types
            msg_type = message.get("type")
            
            if msg_type == "offer":
                # Forward offer to the target user
                target_user = message.get("target")
                if target_user:
                    await connection_manager.send_to_user(
                        room_id, target_user, {
                            "type": "offer",
                            "from": username,
                            "sdp": message.get("sdp")
                        }
                    )
            
            elif msg_type == "answer":
                # Forward answer to the target user
                target_user = message.get("target")
                if target_user:
                    await connection_manager.send_to_user(
                        room_id, target_user, {
                            "type": "answer",
                            "from": username,
                            "sdp": message.get("sdp")
                        }
                    )
            
            elif msg_type == "candidate":
                # Forward ICE candidate to the target user
                target_user = message.get("target")
                if target_user:
                    await connection_manager.send_to_user(
                        room_id, target_user, {
                            "type": "candidate",
                            "from": username,
                            "candidate": message.get("candidate")
                        }
                    )
            
            elif msg_type == "heartbeat":
                # Respond to heartbeat
                await connection_manager.send_personal_message({
                    "type": "heartbeat_response"
                }, websocket)
                
    except WebSocketDisconnect:
        # Handle client disconnection
        connection_manager.disconnect(username, room_id)
        # Notify others that user left
        await connection_manager.broadcast_to_room(room_id, {
            "type": "user_left",
            "username": username,
            "room_id": room_id
        })
    except Exception as e:
        print(f"Error in websocket connection: {e}")
        connection_manager.disconnect(username, room_id)
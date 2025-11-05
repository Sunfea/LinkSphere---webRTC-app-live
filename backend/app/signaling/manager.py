import asyncio
import json
import redis
from typing import Dict, Set, List, Optional
from fastapi import WebSocket
from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.models.database_models import Room, User
from app.utils.database import get_db

class ConnectionManager:
    def __init__(self):
        # Store active connections per room
        self.rooms: Dict[str, Dict[str, WebSocket]] = {}
        # Store user IDs per room
        self.room_users: Dict[str, Set[str]] = {}
        # Redis connection for distributed state (optional)
        try:
            self.redis_client = redis.Redis.from_url("redis://localhost:6379", socket_connect_timeout=1)
            self.redis_client.ping()
            print("Redis connection established")
        except Exception as e:
            self.redis_client = None
            print(f"Redis not available, using in-memory storage: {e}")

    def get_db(self):
        """Get database session"""
        db = SessionLocal()
        try:
            yield db
        finally:
            db.close()

    async def connect(self, websocket: WebSocket, username: str, room_id: str):
        """Connect a user to a room"""
        await websocket.accept()
        
        # Initialize room if it doesn't exist
        if room_id not in self.rooms:
            self.rooms[room_id] = {}
            self.room_users[room_id] = set()
        
        # Add user to room
        self.rooms[room_id][username] = websocket
        self.room_users[room_id].add(username)
        
        # Update room participants in database
        try:
            db = next(self.get_db())
            room = db.query(Room).filter(Room.room_id == room_id).first()
            if room:
                user = db.query(User).filter(User.username == username).first()
                if user and user not in room.participants:
                    room.participants.append(user)
                    db.commit()
        except Exception as e:
            print(f"Database error in connect: {e}")
        
        # Notify others in the room that a user joined
        await self.broadcast_to_room(room_id, {
            "type": "user_joined",
            "username": username,
            "room_id": room_id
        }, exclude=username)

    def disconnect(self, username: str, room_id: str):
        """Disconnect a user from a room"""
        if room_id in self.rooms and username in self.rooms[room_id]:
            del self.rooms[room_id][username]
            self.room_users[room_id].discard(username)
            
            # Update room participants in database
            try:
                db = next(self.get_db())
                room = db.query(Room).filter(Room.room_id == room_id).first()
                if room:
                    user = db.query(User).filter(User.username == username).first()
                    if user and user in room.participants:
                        room.participants.remove(user)
                        db.commit()
            except Exception as e:
                print(f"Database error in disconnect: {e}")
            
            # Clean up empty rooms
            if not self.rooms[room_id]:
                del self.rooms[room_id]
                del self.room_users[room_id]
            
            return True
        return False

    async def send_personal_message(self, message: dict, websocket: WebSocket):
        """Send a message to a specific websocket"""
        try:
            await websocket.send_text(json.dumps(message))
        except Exception as e:
            print(f"Error sending message: {e}")

    async def broadcast_to_room(self, room_id: str, message: dict, exclude: Optional[str] = None):
        """Broadcast a message to all users in a room"""
        if room_id in self.rooms:
            disconnected_users = []
            for username, websocket in self.rooms[room_id].items():
                if exclude is None or username != exclude:
                    try:
                        await self.send_personal_message(message, websocket)
                    except Exception:
                        # Mark user as disconnected if sending fails
                        disconnected_users.append(username)
            
            # Clean up disconnected users
            for username in disconnected_users:
                self.disconnect(username, room_id)

    async def send_to_user(self, room_id: str, username: str, message: dict):
        """Send a message to a specific user in a room"""
        if room_id in self.rooms and username in self.rooms[room_id]:
            try:
                await self.send_personal_message(message, self.rooms[room_id][username])
            except Exception:
                # Clean up if user is disconnected
                self.disconnect(username, room_id)

    def get_room_users(self, room_id: str) -> List[str]:
        """Get list of usernames in a room"""
        if room_id in self.room_users:
            return list(self.room_users[room_id])
        return []

    def get_user_rooms(self, username: str) -> List[str]:
        """Get list of rooms a user is in"""
        rooms = []
        for room_id, users in self.room_users.items():
            if username in users:
                rooms.append(room_id)
        return rooms

connection_manager = ConnectionManager()
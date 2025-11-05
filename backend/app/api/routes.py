from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordRequestForm
from typing import List
import uuid
from app.models.user import User, UserCreate, Token
from app.schemas.room import RoomCreate, RoomWithParticipants
from app.utils.security import verify_password, get_password_hash, create_access_token
from app.api.dependencies import get_current_user
from datetime import datetime, timedelta
from app.core.config import settings

router = APIRouter()

# Mock database storage
fake_users_db = {
    "testuser": {
        "id": 1,
        "username": "testuser",
        "email": "test@example.com",
        "hashed_password": get_password_hash("testpassword"),
        "is_verified": True,
        "created_at": datetime.now()
    }
}

fake_rooms_db = {}

@router.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    """Authenticate user and return access token"""
    user = fake_users_db.get(form_data.username)
    if not user or not verify_password(form_data.password, user["hashed_password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user["username"]}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/users/", response_model=User)
async def create_user(user: UserCreate):
    """Create a new user"""
    if user.username in fake_users_db:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered"
        )
    
    hashed_password = get_password_hash(user.password)
    db_user = {
        "id": len(fake_users_db) + 1,
        "username": user.username,
        "email": user.email,
        "hashed_password": hashed_password,
        "is_verified": True,
        "created_at": datetime.now()
    }
    fake_users_db[user.username] = db_user
    return User(**db_user)

@router.get("/users/me/", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_user)):
    """Get current authenticated user"""
    return current_user

@router.post("/rooms/", response_model=RoomWithParticipants)
async def create_room(room: RoomCreate, current_user: User = Depends(get_current_user)):
    """Create a new room"""
    room_id = str(uuid.uuid4())
    db_room = {
        "id": room_id,
        "name": room.name,
        "description": room.description,
        "owner_id": current_user.id,
        "created_at": datetime.now(),
        "participants": [current_user.username]
    }
    fake_rooms_db[room_id] = db_room
    return RoomWithParticipants(**db_room)

@router.get("/rooms/", response_model=List[RoomWithParticipants])
async def list_rooms(current_user: User = Depends(get_current_user)):
    """List all rooms"""
    return [RoomWithParticipants(**room) for room in fake_rooms_db.values()]

@router.get("/rooms/{room_id}", response_model=RoomWithParticipants)
async def get_room(room_id: str, current_user: User = Depends(get_current_user)):
    """Get details of a specific room"""
    if room_id not in fake_rooms_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Room not found"
        )
    return RoomWithParticipants(**fake_rooms_db[room_id])

@router.post("/rooms/{room_id}/join", response_model=RoomWithParticipants)
async def join_room(room_id: str, current_user: User = Depends(get_current_user)):
    """Join a room"""
    if room_id not in fake_rooms_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Room not found"
        )
    
    room = fake_rooms_db[room_id]
    if current_user.username not in room["participants"]:
        room["participants"].append(current_user.username)
    
    return RoomWithParticipants(**room)

@router.post("/rooms/{room_id}/leave", response_model=RoomWithParticipants)
async def leave_room(room_id: str, current_user: User = Depends(get_current_user)):
    """Leave a room"""
    if room_id not in fake_rooms_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Room not found"
        )
    
    room = fake_rooms_db[room_id]
    if current_user.username in room["participants"]:
        room["participants"].remove(current_user.username)
    
    return RoomWithParticipants(**room)
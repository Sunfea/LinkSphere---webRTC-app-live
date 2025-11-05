from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.orm import Session
import uuid
from datetime import datetime
from app.utils.database import get_db
from app.core.auth_middleware import get_current_user
from app.models.database_models import Room, User
from app.schemas.room import RoomCreate, RoomWithParticipants

router = APIRouter(prefix="/rooms", tags=["Rooms"])

def convert_to_python_types(room_obj):
    """Convert SQLAlchemy model to Python types for Pydantic model"""
    return {
        "id": int(str(room_obj.id)),
        "room_id": str(room_obj.room_id),
        "name": str(room_obj.name),
        "description": str(room_obj.description) if room_obj.description else None,
        "owner_id": int(str(room_obj.owner_id)),
        "created_at": room_obj.created_at,
        "participants": [str(user.username) if user.username else "" for user in room_obj.participants] if hasattr(room_obj, 'participants') else []
    }

@router.post("/", response_model=RoomWithParticipants)
async def create_room(
    room: RoomCreate, 
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new room"""
    # Generate unique room ID
    room_id = str(uuid.uuid4())
    
    # Create room in database
    db_room = Room(
        room_id=room_id,
        name=room.name,
        description=room.description,
        owner_id=current_user.id
    )
    db.add(db_room)
    db.commit()
    db.refresh(db_room)
    
    # Convert to Python types
    room_data = convert_to_python_types(db_room)
    username = str(current_user.username) if current_user.username is not None else ""
    room_data["participants"] = [username]
    
    return RoomWithParticipants(**room_data)

@router.get("/", response_model=list[RoomWithParticipants])
async def list_rooms(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """List all available rooms"""
    # Get all rooms
    rooms = db.query(Room).all()
    
    result = []
    for room in rooms:
        room_data = convert_to_python_types(room)
        result.append(RoomWithParticipants(**room_data))
    
    return result

@router.get("/{room_id}", response_model=RoomWithParticipants)
async def get_room(
    room_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get details of a specific room"""
    room = db.query(Room).filter(Room.room_id == room_id).first()
    if not room:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Room not found"
        )
    
    # Check if user is participant
    if current_user not in room.participants:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not a participant in this room"
        )
    
    room_data = convert_to_python_types(room)
    return RoomWithParticipants(**room_data)

@router.post("/{room_id}/join", response_model=RoomWithParticipants)
async def join_room(
    room_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Join a room"""
    room = db.query(Room).filter(Room.room_id == room_id).first()
    if not room:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Room not found"
        )
    
    # Add user to room participants if not already in
    if current_user not in room.participants:
        room.participants.append(current_user)
        db.commit()
    
    room_data = convert_to_python_types(room)
    return RoomWithParticipants(**room_data)

@router.post("/{room_id}/leave", response_model=RoomWithParticipants)
async def leave_room(
    room_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Leave a room"""
    room = db.query(Room).filter(Room.room_id == room_id).first()
    if not room:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Room not found"
        )
    
    # Remove user from room participants if in room
    if current_user in room.participants:
        room.participants.remove(current_user)
        db.commit()
    
    room_data = convert_to_python_types(room)
    return RoomWithParticipants(**room_data)
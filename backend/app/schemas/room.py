from pydantic import BaseModel, ConfigDict
from typing import List, Optional
from datetime import datetime

class RoomBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    name: str
    description: Optional[str] = None

class RoomCreate(RoomBase):
    pass

class Room(RoomBase):
    id: int
    room_id: str
    owner_id: int
    created_at: datetime

class RoomWithParticipants(Room):
    participants: List[str] = []
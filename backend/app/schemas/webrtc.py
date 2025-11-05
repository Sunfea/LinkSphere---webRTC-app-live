from pydantic import BaseModel, ConfigDict
from typing import Optional, Dict, Any

class WebRTCSignaling(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    type: str  # "offer", "answer", "candidate", "join", "leave"
    data: Dict[str, Any] = {}
    sender: str  # sender's user ID
    recipient: Optional[str] = None  # recipient's user ID (for direct messages)
    room: Optional[str] = None  # room ID

class Offer(WebRTCSignaling):
    model_config = ConfigDict(from_attributes=True)
    
    type: str = "offer"
    sdp: str
    room: str  # type: ignore

class Answer(WebRTCSignaling):
    model_config = ConfigDict(from_attributes=True)
    
    type: str = "answer"
    sdp: str
    room: str  # type: ignore

class IceCandidate(WebRTCSignaling):
    model_config = ConfigDict(from_attributes=True)
    
    type: str = "candidate"
    candidate: Dict[str, Any]
    room: str  # type: ignore

class JoinRoom(WebRTCSignaling):
    model_config = ConfigDict(from_attributes=True)
    
    type: str = "join"
    room: str  # type: ignore

class LeaveRoom(WebRTCSignaling):
    model_config = ConfigDict(from_attributes=True)
    
    type: str = "leave"
    room: str  # type: ignore
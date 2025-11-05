from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Table
from sqlalchemy.orm import relationship
from datetime import datetime
from app.core.database import Base
from typing import List

# Association table for Room-User many-to-many relationship
room_participants = Table(
    "room_participants",
    Base.metadata,
    Column("room_id", Integer, ForeignKey("rooms.id")),
    Column("user_id", Integer, ForeignKey("users.id"))
)

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    is_verified = Column(Boolean, default=False)
    username = Column(String, unique=True, index=True, nullable=True)
    hashed_password = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationship to rooms where this user is a participant
    rooms = relationship("Room", secondary=room_participants, back_populates="participants")

class OTP(Base):
    __tablename__ = "otps"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, index=True, nullable=False)
    otp = Column(String, nullable=False)
    expiry = Column(DateTime, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

class Room(Base):
    __tablename__ = "rooms"
    
    id = Column(Integer, primary_key=True, index=True)
    room_id = Column(String, unique=True, index=True, nullable=False)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    owner_id = Column(Integer, ForeignKey("users.id"))
    
    # Relationship to participants
    participants = relationship("User", secondary=room_participants, back_populates="rooms")
    
    # Relationship to owner
    owner = relationship("User")
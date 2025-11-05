from pydantic import BaseModel, EmailStr, ConfigDict
from typing import Optional
from datetime import datetime

# Base user model
class UserBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    email: EmailStr

# Model for user creation (signup)
class UserCreate(UserBase):
    model_config = ConfigDict(from_attributes=True)
    
    username: str
    password: str

# Model for setting username
class UsernameSet(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    email: EmailStr
    username: str

# Model for OTP verification
class OTPVerify(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    email: EmailStr
    otp: str

# Model for login
class UserLogin(UserBase):
    model_config = ConfigDict(from_attributes=True)
    
    pass

# Response model for user
class User(UserBase):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    is_verified: bool
    username: Optional[str] = None
    created_at: datetime

# Model for user in database (with hashed password)
class UserInDB(User):
    model_config = ConfigDict(from_attributes=True)
    
    hashed_password: str

# Token models
class Token(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    access_token: str
    token_type: str

class TokenData(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    username: Optional[str] = None
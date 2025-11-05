from pydantic import BaseModel, EmailStr, ConfigDict
from typing import Optional
from datetime import datetime

# Schema for signup request
class SignupRequest(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    email: EmailStr

# Schema for OTP verification request
class VerifyOTPRequest(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    email: EmailStr
    otp: str

# Schema for setting username request
class SetUsernameRequest(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    email: EmailStr
    username: str

# Schema for login request
class LoginRequest(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    email: EmailStr

# Schema for OTP response
class OTPResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    message: str

# Schema for user response
class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    email: EmailStr
    is_verified: bool
    username: Optional[str] = None
    created_at: datetime

# Schema for token response
class TokenResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    access_token: str
    token_type: str
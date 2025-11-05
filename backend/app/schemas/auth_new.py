from pydantic import BaseModel, EmailStr, ConfigDict
from typing import Optional
from datetime import datetime

# Schema for register request
class RegisterRequest(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    email: EmailStr
    password: str

# Schema for OTP verification request
class VerifyOTPRequest(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    email: EmailStr
    otp: str

# Schema for login request
class LoginRequest(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    username: str
    password: str

# Schema for OTP response
class OTPResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    message: str

# Schema for register response
class RegisterResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    message: str
    email: EmailStr

# Schema for login response
class LoginResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    access_token: str
    token_type: str
    username: str

# Schema for user response
class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    email: EmailStr
    is_verified: bool
    username: Optional[str] = None
    created_at: datetime
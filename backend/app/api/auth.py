from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
import re
from app.utils.database import get_db
from app.utils.auth import generate_otp, create_access_token
from app.utils.email import send_otp_email
from app.models.database_models import User, OTP
from app.schemas.auth import (
    SignupRequest, 
    VerifyOTPRequest, 
    SetUsernameRequest, 
    LoginRequest, 
    OTPResponse, 
    TokenResponse
)
from app.core.config import settings

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/signup", response_model=OTPResponse)
async def signup(request: SignupRequest, db: Session = Depends(get_db)):
    """Signup endpoint - accepts email, generates and stores OTP, sends OTP to email"""
    
    # Check if user already exists
    existing_user = db.query(User).filter(User.email == request.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email already exists"
        )
    
    # Generate OTP
    otp_code = generate_otp()
    expiry = datetime.utcnow() + timedelta(minutes=10)  # OTP expires in 10 minutes
    
    # Store OTP in database
    otp_record = OTP(
        email=request.email,
        otp=otp_code,
        expiry=expiry
    )
    db.add(otp_record)
    
    # Create user with is_verified = False
    new_user = User(
        email=request.email,
        is_verified=False
    )
    db.add(new_user)
    
    # Commit changes
    db.commit()
    
    # Send OTP to email (in development, this will be printed to console)
    send_otp_email(request.email, otp_code)
    
    return OTPResponse(message="OTP sent to your email")

@router.post("/verify-otp", response_model=OTPResponse)
async def verify_otp(request: VerifyOTPRequest, db: Session = Depends(get_db)):
    """Verify OTP endpoint - accepts email + OTP, verifies OTP and sets is_verified = True"""
    
    # Find OTP record
    otp_record = db.query(OTP).filter(
        OTP.email == request.email,
        OTP.otp == request.otp
    ).first()
    
    # Check if OTP exists and is not expired
    if not otp_record:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid OTP"
        )
        
    if otp_record.expiry.replace(tzinfo=None) < datetime.utcnow():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Expired OTP"
        )
    
    # Find user
    user = db.query(User).filter(User.email == request.email).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Set user as verified using setattr for proper SQLAlchemy handling
    setattr(user, 'is_verified', True)
    
    # Delete OTP record
    db.delete(otp_record)
    
    # Commit changes
    db.commit()
    db.refresh(user)
    
    return OTPResponse(message="OTP verified successfully")

@router.post("/set-username", response_model=OTPResponse)
async def set_username(request: SetUsernameRequest, db: Session = Depends(get_db)):
    """Set username endpoint - accepts email + desired username, validates and stores username"""
    
    # Validate username format (lowercase, alphanumeric)
    if not re.match("^[a-z0-9]+$", request.username):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username must be lowercase and alphanumeric"
        )
    
    # Check if username is already taken
    existing_user = db.query(User).filter(User.username == request.username).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already taken"
        )
    
    # Find user by email
    user = db.query(User).filter(User.email == request.email).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Set username using setattr for proper SQLAlchemy handling
    setattr(user, 'username', request.username)
    
    # Commit changes
    db.commit()
    db.refresh(user)
    
    return OTPResponse(message="Username set successfully")

@router.post("/login", response_model=TokenResponse)
async def login(request: LoginRequest, db: Session = Depends(get_db)):
    """Login endpoint - accepts email, returns JWT token if email is verified"""
    
    # Find user
    user = db.query(User).filter(User.email == request.email).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Check if user is verified (access attribute value properly)
    if not bool(getattr(user, 'is_verified', False)):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email not verified"
        )
    
    # Check if user has set a username
    if not getattr(user, 'username', None):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username not set"
        )
    
    # Create access token
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": getattr(user, 'username')}, 
        expires_delta=access_token_expires
    )
    
    return TokenResponse(
        access_token=access_token,
        token_type="bearer"
    )
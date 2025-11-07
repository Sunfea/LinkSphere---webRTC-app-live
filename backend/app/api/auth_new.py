from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
import re
import secrets
import string
from app.utils.database import get_db
from app.utils.auth import generate_otp, create_access_token, get_password_hash, verify_password
from app.utils.email import send_otp_email, send_username_email
from app.models.database_models import User, OTP
from app.schemas.auth_new import (
    RegisterRequest, 
    VerifyOTPRequest, 
    LoginRequest, 
    OTPResponse, 
    RegisterResponse, 
    LoginResponse,
    UserResponse
)
from app.core.config import settings
from app.core.auth_middleware import get_current_user

router = APIRouter(prefix="/auth", tags=["Authentication"])

def generate_unique_username(db: Session, email: str) -> str:
    """Generate a unique, lowercase, alphanumeric username"""
    # Extract local part of email (before @)
    local_part = email.split('@')[0].lower()
    
    # Remove non-alphanumeric characters
    base_username = re.sub(r'[^a-z0-9]', '', local_part)
    
    # If username is too short, pad with random characters
    if len(base_username) < 3:
        base_username = base_username + ''.join(secrets.choice(string.ascii_lowercase + string.digits) for _ in range(3 - len(base_username)))
    
    # Ensure username is not too long
    base_username = base_username[:15]
    
    # Check if base username is available
    user = db.query(User).filter(User.username == base_username).first()
    if not user:
        return base_username
    
    # If not available, try with numbers
    for i in range(100):
        username = f"{base_username}{i}"
        user = db.query(User).filter(User.username == username).first()
        if not user:
            return username
    
    # If still not available, generate random username
    for i in range(100):
        username = ''.join(secrets.choice(string.ascii_lowercase + string.digits) for _ in range(8))
        user = db.query(User).filter(User.username == username).first()
        if not user:
            return username
    
    # Fallback (should never happen)
    return f"user{secrets.token_hex(4)}"

@router.post("/register", response_model=RegisterResponse)
async def register(request: RegisterRequest, db: Session = Depends(get_db)):
    """Register endpoint - accepts email and password, generates and stores OTP"""
    
    # Validate that email ends with @gmail.com
    if not request.email.endswith('@gmail.com'):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email must be a Gmail address (end with @gmail.com)"
        )
    
    # Check if user already exists
    existing_user = db.query(User).filter(User.email == request.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email already exists"
        )
    
    # Hash password
    hashed_password = get_password_hash(request.password)
    
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
        hashed_password=hashed_password,
        is_verified=False
    )
    db.add(new_user)
    
    # Commit changes
    db.commit()
    
    # Send OTP to email (in development, this will be printed to console)
    send_otp_email(request.email, otp_code)
    
    return RegisterResponse(
        message="OTP sent to your email. Please verify to complete registration.",
        email=request.email
    )

@router.post("/verify-otp", response_model=OTPResponse)
async def verify_otp(request: VerifyOTPRequest, db: Session = Depends(get_db)):
    """Verify OTP endpoint - accepts email + OTP, verifies OTP and sets is_verified = True"""
    
    # Validate that email ends with @gmail.com
    if not request.email.endswith('@gmail.com'):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email must be a Gmail address (end with @gmail.com)"
        )
    
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
    
    # Set user as verified
    setattr(user, 'is_verified', True)
    
    # Generate unique username
    username = generate_unique_username(db, request.email)
    setattr(user, 'username', username)
    
    # Delete OTP record
    db.delete(otp_record)
    
    # Commit changes
    db.commit()
    db.refresh(user)
    
    # Send username to user via email
    send_username_email(request.email, username)
    
    return OTPResponse(message=f"Email verified successfully. Your username is: {username}")

@router.post("/login", response_model=LoginResponse)
async def login(request: LoginRequest, db: Session = Depends(get_db)):
    """Login endpoint - accepts username and password, returns JWT token"""
    
    # Find user by username
    user = db.query(User).filter(User.username == request.username).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Verify password
    if not verify_password(request.password, getattr(user, 'hashed_password', '') or ""):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect password"
        )
    
    # Check if user is verified
    if not getattr(user, 'is_verified', False):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email not verified"
        )
    
    # Create access token
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": getattr(user, 'username', '')}, 
        expires_delta=access_token_expires
    )
    
    return LoginResponse(
        access_token=access_token,
        token_type="bearer",
        username=getattr(user, 'username', '')
    )

@router.get("/me", response_model=UserResponse)
async def get_current_user_endpoint(current_user: User = Depends(get_current_user)):
    """Get current user information"""
    return current_user
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from typing import Optional
from datetime import datetime
from app.utils.security import decode_access_token
from app.models.user import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/token")

async def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    token_data = decode_access_token(token)
    if token_data is None or token_data.username is None:
        raise credentials_exception
    # In a real app, you would fetch the user from a database
    # For now, we'll create a mock user
    user = User(
        id=1,
        username=token_data.username,
        email=f"{token_data.username}@example.com",
        is_verified=True,
        created_at=datetime.now()
    )
    return user
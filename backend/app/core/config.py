import os
from typing import List
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Application settings
    PROJECT_NAME: str = "WebRTC Communication App"
    DEBUG: bool = False
    VERSION: str = "1.0.0"
    
    # Server settings
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    
    # Security settings
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your-secret-key-here")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # CORS settings
    BACKEND_CORS_ORIGINS: List[str] = ["*"]
    
    # Database settings
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./test.db")
    
    # Redis settings (optional)
    REDIS_HOST: str = os.getenv("REDIS_HOST", "localhost")
    REDIS_PORT: int = int(os.getenv("REDIS_PORT", 6379))
    REDIS_DB: int = int(os.getenv("REDIS_DB", 0))
    REDIS_URL: str = os.getenv("REDIS_URL", "redis://localhost:6379")
    
    # Email settings (for OTP)
    SMTP_SERVER: str = os.getenv("SMTP_SERVER", "localhost")
    SMTP_PORT: int = int(os.getenv("SMTP_PORT", 1025))
    EMAIL_USER: str = os.getenv("EMAIL_USER", "test@example.com")
    EMAIL_PASSWORD: str = os.getenv("EMAIL_PASSWORD", "password")
    
    class Config:
        case_sensitive = True
        env_file = ".env"

settings = Settings()
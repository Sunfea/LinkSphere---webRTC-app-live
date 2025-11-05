from app.core.database import SessionLocal
from typing import Generator

def get_db() -> Generator:
    """Dependency to get DB session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
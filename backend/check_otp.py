#!/usr/bin/env python3
"""
Script to check OTP records in the database
"""

from app.core.database import SessionLocal
from app.models.database_models import OTP, User

def check_otp_records():
    """Check OTP records in the database"""
    db = SessionLocal()
    try:
        # Get all OTP records
        otp_records = db.query(OTP).all()
        print(f"Found {len(otp_records)} OTP records:")
        for otp in otp_records:
            print(f"  Email: {otp.email}, OTP: {otp.otp}, Expiry: {otp.expiry}")
        
        # Get all users
        users = db.query(User).all()
        print(f"\nFound {len(users)} users:")
        for user in users:
            print(f"  Email: {user.email}, Verified: {user.is_verified}, Username: {user.username}")
    finally:
        db.close()

if __name__ == "__main__":
    check_otp_records()
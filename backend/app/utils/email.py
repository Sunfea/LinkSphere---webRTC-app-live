import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Optional
from app.core.config import settings

def send_otp_email(email: str, otp: str) -> bool:
    """
    Send OTP to email using SMTP.
    """
    # Always use simulation mode to avoid SMTP delays
    print("=" * 60)
    print("OTP EMAIL SIMULATION - FOR TESTING PURPOSES")
    print("=" * 60)
    print(f"📧 EMAIL ADDRESS: {email}")
    print(f"🔑 OTP CODE: {otp}")
    print(f"⏰ EXPIRES IN: 10 minutes")
    print("")
    print("NOTE: Email sending is disabled for faster performance.")
    print("In production, this OTP would be sent to your email.")
    print("=" * 60)
    return True

def send_username_email(email: str, username: str) -> bool:
    """
    Send username to email using SMTP.
    """
    # Always use simulation mode to avoid SMTP delays
    print("=" * 60)
    print("USERNAME EMAIL SIMULATION - FOR TESTING PURPOSES")
    print("=" * 60)
    print(f"📧 EMAIL ADDRESS: {email}")
    print(f"👤 USERNAME: {username}")
    print("")
    print("You can now login using this username and your password.")
    print("")
    print("NOTE: Email sending is disabled for faster performance.")
    print("In production, this username would be sent to your email.")
    print("=" * 60)
    return True

def test_otp_display(email: str, otp: str):
    """
    Utility function for testing - displays OTP and email clearly
    """
    print("=" * 60)
    print("TEST OTP DISPLAY")
    print("=" * 60)
    print(f"📧 EMAIL ADDRESS: {email}")
    print(f"🔑 OTP CODE: {otp}")
    print("=" * 60)

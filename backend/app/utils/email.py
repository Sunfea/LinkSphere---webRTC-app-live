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
    try:
        # Check if we're in development mode
        if settings.DEBUG or settings.SMTP_HOST == "localhost":
            # For development, just print to console with a clear message
            print("=" * 60)
            print("OTP EMAIL SIMULATION - FOR TESTING PURPOSES")
            print("=" * 60)
            print(f"📧 EMAIL ADDRESS: {email}")
            print(f"🔑 OTP CODE: {otp}")
            print(f"⏰ EXPIRES IN: 10 minutes")
            print("")
            print("NOTE: This is a development environment.")
            print("In production, this OTP would be sent to your email.")
            print("=" * 60)
            return True
        
        # In production, use SMTP to send real emails
        msg = MIMEMultipart()
        msg['From'] = settings.SMTP_USER
        msg['To'] = email
        msg['Subject'] = "Your OTP Code for WebRTC App"
        
        body = f"""
Hello,

Your OTP code for WebRTC App is: {otp}

This code will expire in 10 minutes.

If you didn't request this code, please ignore this email.

Best regards,
WebRTC App Team
        """
        msg.attach(MIMEText(body, 'plain'))
        
        server = smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT)
        server.starttls()
        server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
        text = msg.as_string()
        server.sendmail(settings.SMTP_USER, email, text)
        server.quit()
        
        return True
    except Exception as e:
        print(f"Error sending email: {e}")
        return False

def send_username_email(email: str, username: str) -> bool:
    """
    Send username to email using SMTP.
    """
    try:
        # Check if we're in development mode
        if settings.DEBUG or settings.SMTP_HOST == "localhost":
            # For development, just print to console with a clear message
            print("=" * 60)
            print("USERNAME EMAIL SIMULATION - FOR TESTING PURPOSES")
            print("=" * 60)
            print(f"📧 EMAIL ADDRESS: {email}")
            print(f"👤 USERNAME: {username}")
            print("")
            print("You can now login using this username and your password.")
            print("")
            print("NOTE: This is a development environment.")
            print("In production, this username would be sent to your email.")
            print("=" * 60)
            return True
        
        # In production, use SMTP to send real emails
        msg = MIMEMultipart()
        msg['From'] = settings.SMTP_USER
        msg['To'] = email
        msg['Subject'] = "Your Username for WebRTC App"
        
        body = f"""
Hello,

Your username for WebRTC App is: {username}

You can now login using this username and your password.

Best regards,
WebRTC App Team
        """
        msg.attach(MIMEText(body, 'plain'))
        
        server = smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT)
        server.starttls()
        server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
        text = msg.as_string()
        server.sendmail(settings.SMTP_USER, email, text)
        server.quit()
        
        return True
    except Exception as e:
        print(f"Error sending email: {e}")
        return False

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

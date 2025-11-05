import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Optional

def send_otp_email(email: str, otp: str) -> bool:
    """
    Send OTP to email. In production, this would use SMTP.
    For development, we'll just print to console.
    """
    try:
        # For development, just print to console with a clear message
        print("=" * 50)
        print(f"OTP EMAIL SIMULATION")
        print(f"To: {email}")
        print(f"Subject: Your OTP Code")
        print(f"")
        print(f"Your OTP code is: {otp}")
        print(f"")
        print(f"NOTE: This is a development environment.")
        print(f"In production, this OTP would be sent to your email.")
        print("=" * 50)
        
        # In production, you would use SMTP:
        """
        smtp_server = os.getenv("SMTP_SERVER")
        smtp_port = int(os.getenv("SMTP_PORT", 587))
        email_user = os.getenv("EMAIL_USER")
        email_password = os.getenv("EMAIL_PASSWORD")
        
        msg = MIMEMultipart()
        msg['From'] = email_user
        msg['To'] = email
        msg['Subject'] = "Your OTP Code"
        
        body = f"Your OTP code is: {otp}"
        msg.attach(MIMEText(body, 'plain'))
        
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(email_user, email_password)
        text = msg.as_string()
        server.sendmail(email_user, email, text)
        server.quit()
        """
        
        return True
    except Exception as e:
        print(f"Error sending email: {e}")
        return False

def send_username_email(email: str, username: str) -> bool:
    """
    Send username to email. In production, this would use SMTP.
    For development, we'll just print to console.
    """
    try:
        # For development, just print to console with a clear message
        print("=" * 50)
        print(f"USERNAME EMAIL SIMULATION")
        print(f"To: {email}")
        print(f"Subject: Your Username")
        print(f"")
        print(f"Your username is: {username}")
        print(f"You can now login using this username and your password.")
        print(f"")
        print(f"NOTE: This is a development environment.")
        print(f"In production, this username would be sent to your email.")
        print("=" * 50)
        
        # In production, you would use SMTP:
        """
        smtp_server = os.getenv("SMTP_SERVER")
        smtp_port = int(os.getenv("SMTP_PORT", 587))
        email_user = os.getenv("EMAIL_USER")
        email_password = os.getenv("EMAIL_PASSWORD")
        
        msg = MIMEMultipart()
        msg['From'] = email_user
        msg['To'] = email
        msg['Subject'] = "Your Username"
        
        body = f"Your username is: {username}\nYou can now login using this username and your password."
        msg.attach(MIMEText(body, 'plain'))
        
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(email_user, email_password)
        text = msg.as_string()
        server.sendmail(email_user, email, text)
        server.quit()
        """
        
        return True
    except Exception as e:
        print(f"Error sending email: {e}")
        return False
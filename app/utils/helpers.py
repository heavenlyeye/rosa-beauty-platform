import re
import logging
from typing import Optional
from fastapi import Request

logger = logging.getLogger(__name__)

def get_client_ip(request: Request) -> str:
    """Get client IP address from request"""
    x_forwarded_for = request.headers.get("X-Forwarded-For")
    if x_forwarded_for:
        return x_forwarded_for.split(",")[0].strip()
    
    x_real_ip = request.headers.get("X-Real-IP")
    if x_real_ip:
        return x_real_ip
    
    return request.client.host if request.client else "unknown"

def log_security_event(event: str, ip: str, user: Optional[str] = None, details: Optional[str] = None):
    """Log security events with proper formatting"""
    logger.info(f"SECURITY_EVENT: {event} | IP: {ip} | User: {user or 'N/A'} | Details: {details or 'N/A'}")

def format_phone_number(phone: str) -> str:
    """Format phone number to standard format"""
    if not phone:
        return ""
    
    # Remove all non-digit characters
    digits = re.sub(r'\D', '', phone)
    
    # Handle Iranian phone numbers
    if digits.startswith('98'):
        digits = digits[2:]
    elif digits.startswith('0'):
        digits = digits[1:]
    
    # Format as 09XXXXXXXXX
    if len(digits) == 10:
        return f"0{digits}"
    elif len(digits) == 9:
        return f"0{digits}"
    
    return phone  # Return original if can't format

def sanitize_username(username: str) -> str:
    """Sanitize username - remove special characters"""
    if not username:
        return ""
    
    # Allow only alphanumeric and underscore
    sanitized = re.sub(r'[^a-zA-Z0-9_]', '', username)
    return sanitized.lower()

def format_instagram_handle(instagram: str) -> str:
    """Format Instagram handle"""
    if not instagram:
        return ""
    
    # Remove @ if present
    handle = instagram.lstrip('@')
    
    # Remove instagram.com/ if present
    handle = re.sub(r'.*instagram\.com/', '', handle)
    
    # Remove trailing slash
    handle = handle.rstrip('/')
    
    return handle
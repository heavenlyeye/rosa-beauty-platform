from fastapi import HTTPException, Depends, status
from sqlalchemy.orm import Session
from ..database import get_db
from ..models.user import User, UserRole
from .jwt_handler import verify_token

def require_admin(current_user: User = Depends()):
    """Require admin role"""
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )
    return current_user

def require_salon_owner(current_user: User = Depends()):
    """Require salon owner role"""
    if current_user.role not in [UserRole.SALON_OWNER, UserRole.ADMIN]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Salon owner access required"
        )
    return current_user
from pydantic import BaseModel, Field, validator
from typing import Optional
from datetime import datetime
from enum import Enum

# تعریف محلی UserRole
class UserRole(str, Enum):
    CLIENT = "client"          # مشتری
    SALON_OWNER = "salon_owner"  # صاحب سالن
    STYLIST = "stylist"        # آرایشگر
    ADMIN = "admin"            # ادمین

class UserCreate(BaseModel):
    """اسکیما برای ایجاد کاربر جدید"""
    username: str = Field(..., min_length=3, max_length=50, description="نام کاربری")
    password: str = Field(..., min_length=6, max_length=128, description="رمز عبور")
    full_name: Optional[str] = Field(None, max_length=100, description="نام کامل")
    phone: Optional[str] = Field(None, pattern=r'^09\d{9}$', description="شماره تلفن همراه")
    role: UserRole = Field(UserRole.CLIENT, description="نقش کاربر")

class UserUpdate(BaseModel):
    """اسکیما برای بروزرسانی کاربر"""
    full_name: Optional[str] = Field(None, max_length=100)
    phone: Optional[str] = Field(None, pattern=r'^09\d{9}$')
    is_active: Optional[bool] = None
    is_verified: Optional[bool] = None

class UserRead(BaseModel):
    """اسکیما برای خواندن کاربر"""
    id: int
    username: str
    full_name: Optional[str] = None
    phone: Optional[str] = None
    role: UserRole
    is_active: bool
    is_verified: bool
    created_at: datetime
    last_login: Optional[datetime] = None

    class Config:
        from_attributes = True

class CustomerCreate(BaseModel):
    """اسکیما برای ایجاد مشتری جدید"""
    full_name: str = Field(..., min_length=2, max_length=100, description="نام کامل مشتری")
    phone: str = Field(..., pattern=r'^09\d{9}$', description="شماره تلفن همراه")
    notes: Optional[str] = Field(None, max_length=500, description="یادداشت")

class CustomerRead(BaseModel):
    """اسکیما برای خواندن اطلاعات مشتری"""
    id: int
    full_name: str
    phone: str
    total_visits: int
    total_spent: float
    last_visit: Optional[datetime] = None
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True

# تعریف role names برای استفاده در API
USER_ROLE_NAMES = {
    UserRole.CLIENT: "مشتری",
    UserRole.SALON_OWNER: "صاحب سالن",
    UserRole.STYLIST: "آرایشگر",
    UserRole.ADMIN: "مدیر سیستم"
}

def get_role_name(role: UserRole) -> str:
    """تابع کمکی برای دریافت نام فارسی نقش"""
    return USER_ROLE_NAMES.get(role, "نامشخص")
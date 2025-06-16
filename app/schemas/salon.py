from pydantic import BaseModel, Field, validator
from typing import Optional
from datetime import datetime

class SalonCreate(BaseModel):
    """اسکیما برای ایجاد سالن جدید"""
    username: str = Field(..., min_length=3, max_length=50, description="نام کاربری")
    password: str = Field(..., min_length=6, max_length=128, description="رمز عبور")
    name: str = Field(..., min_length=2, max_length=100, description="نام سالن")
    address: Optional[str] = Field(None, max_length=500, description="آدرس")
    phone: Optional[str] = Field(None, pattern=r'^09\d{9}$', description="شماره تلفن")
    instagram: Optional[str] = Field(None, max_length=100, description="آیدی اینستاگرام")
    description: Optional[str] = Field(None, max_length=1000, description="توضیحات سالن")
    city: Optional[str] = Field(None, max_length=50, description="شهر")
    province: Optional[str] = Field(None, max_length=50, description="استان")

    @validator('username')
    def validate_username(cls, v):
        if not v or v.strip() == "":
            raise ValueError('نام کاربری نمی‌تواند خالی باشد')
        # بررسی کاراکترهای مجاز
        if not v.replace('_', '').replace('.', '').isalnum():
            raise ValueError('نام کاربری فقط می‌تواند شامل حروف، اعداد، _ و . باشد')
        return v.strip().lower()

    @validator('name')
    def validate_name(cls, v):
        if not v or v.strip() == "":
            raise ValueError('نام سالن نمی‌تواند خالی باشد')
        return v.strip()

    @validator('phone')
    def validate_phone(cls, v):
        if v and (not v.startswith('09') or len(v) != 11):
            raise ValueError('شماره تلفن باید 11 رقم باشد و با 09 شروع شود')
        return v

    @validator('instagram')
    def validate_instagram(cls, v):
        if v:
            # حذف @ در صورت وجود
            v = v.strip().lstrip('@')
            # بررسی فرمت آیدی اینستاگرام
            if not v.replace('_', '').replace('.', '').isalnum():
                raise ValueError('آیدی اینستاگرام نامعتبر است')
        return v

    @validator('password')
    def validate_password(cls, v):
        if len(v) < 6:
            raise ValueError('رمز عبور باید حداقل 6 کاراکتر باشد')
        return v

class SalonUpdate(BaseModel):
    """اسکیما برای بروزرسانی سالن"""
    name: Optional[str] = Field(None, min_length=2, max_length=100)
    address: Optional[str] = Field(None, max_length=500)
    phone: Optional[str] = Field(None, pattern=r'^09\d{9}$')
    instagram: Optional[str] = Field(None, max_length=100)
    description: Optional[str] = Field(None, max_length=1000)
    city: Optional[str] = Field(None, max_length=50)
    province: Optional[str] = Field(None, max_length=50)
    is_verified: Optional[bool] = None
    is_active: Optional[bool] = None

    @validator('name')
    def validate_name_update(cls, v):
        if v and (not v or v.strip() == ""):
            raise ValueError('نام سالن نمی‌تواند خالی باشد')
        return v.strip() if v else v

    @validator('phone')
    def validate_phone_update(cls, v):
        if v and (not v.startswith('09') or len(v) != 11):
            raise ValueError('شماره تلفن باید 11 رقم باشد و با 09 شروع شود')
        return v

    @validator('instagram')
    def validate_instagram_update(cls, v):
        if v:
            v = v.strip().lstrip('@')
            if not v.replace('_', '').replace('.', '').isalnum():
                raise ValueError('آیدی اینستاگرام نامعتبر است')
        return v

class SalonRead(BaseModel):
    """اسکیما برای خواندن اطلاعات سالن"""
    id: int
    username: str
    name: str
    address: Optional[str] = None
    phone: Optional[str] = None
    instagram: Optional[str] = None
    description: Optional[str] = None
    city: Optional[str] = None
    province: Optional[str] = None
    is_verified: bool
    is_active: bool
    average_rating: float
    total_ratings: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }

class SalonProfile(BaseModel):
    """اسکیما پروفایل عمومی سالن"""
    id: int
    name: str
    address: Optional[str] = None
    phone: Optional[str] = None
    instagram: Optional[str] = None
    description: Optional[str] = None
    city: Optional[str] = None
    province: Optional[str] = None
    is_verified: bool
    average_rating: float
    total_ratings: int
    services_count: Optional[int] = 0
    is_open: Optional[bool] = True

class SalonStats(BaseModel):
    """اسکیما آمار سالن"""
    total_bookings: int
    completed_bookings: int
    pending_bookings: int
    cancelled_bookings: int
    total_revenue: float
    monthly_revenue: float
    total_customers: int
    active_customers: int
    services_count: int
    average_rating: float
    completion_rate: float

class SalonResponse(BaseModel):
    """اسکیما پاسخ عمومی برای عملیات سالن"""
    message: str
    salon_id: Optional[int] = None
    success: bool = True

class SalonLogin(BaseModel):
    """اسکیما ورود سالن"""
    username: str = Field(..., description="نام کاربری")
    password: str = Field(..., description="رمز عبور")
    remember_me: bool = Field(False, description="مرا به خاطر بسپار")

class SalonPasswordUpdate(BaseModel):
    """اسکیما تغییر رمز عبور سالن"""
    current_password: str = Field(..., description="رمز عبور فعلی")
    new_password: str = Field(..., min_length=6, max_length=128, description="رمز عبور جدید")
    confirm_password: str = Field(..., description="تکرار رمز عبور جدید")

    @validator('confirm_password')
    def validate_passwords_match(cls, v, values):
        if 'new_password' in values and v != values['new_password']:
            raise ValueError('تکرار رمز عبور با رمز عبور جدید مطابقت ندارد')
        return v

    @validator('new_password')
    def validate_new_password(cls, v, values):
        if 'current_password' in values and v == values['current_password']:
            raise ValueError('رمز عبور جدید باید متفاوت از رمز عبور فعلی باشد')
        if len(v) < 6:
            raise ValueError('رمز عبور جدید باید حداقل 6 کاراکتر باشد')
        return v
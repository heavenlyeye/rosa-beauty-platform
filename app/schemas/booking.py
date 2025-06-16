from pydantic import BaseModel, Field, validator
from typing import Optional
from datetime import datetime
from enum import Enum

# تعریف محلی BookingStatus
class BookingStatus(str, Enum):
    PENDING = "pending"        # در انتظار تایید
    CONFIRMED = "confirmed"    # تایید شده
    IN_PROGRESS = "in_progress"  # در حال انجام
    COMPLETED = "completed"    # تکمیل شده
    CANCELLED = "cancelled"    # لغو شده
    NO_SHOW = "no_show"       # عدم حضور

class BookingCreate(BaseModel):
    """اسکیما برای ایجاد نوبت (روش قدیمی)"""
    booking_date: datetime
    notes: Optional[str] = None
    customer_id: int
    salon_id: int
    service_id: int
    stylist_id: Optional[int] = None

class BookingCreateFromForm(BaseModel):
    """اسکیما برای ایجاد نوبت از فرم داشبورد"""
    customer_name: str = Field(..., min_length=2, max_length=100, description="نام مشتری")
    customer_phone: str = Field(..., pattern=r'^09\d{9}$', description="شماره تلفن همراه")
    booking_date: str = Field(..., description="تاریخ و زمان نوبت (ISO format)")
    service_id: int = Field(..., gt=0, description="شناسه خدمت")
    notes: Optional[str] = Field(None, max_length=500, description="یادداشت")
    payment_method: Optional[str] = Field(None, description="روش پرداخت")
    paid_amount: Optional[float] = Field(0, ge=0, description="مبلغ پرداخت شده")

class BookingRead(BaseModel):
    """اسکیما برای خواندن نوبت"""
    id: int
    booking_date: datetime
    status: BookingStatus
    notes: Optional[str] = None
    total_price: float
    paid_amount: float = 0.0
    is_paid: bool = False
    payment_method: Optional[str] = None
    customer_id: int
    salon_id: int
    service_id: int
    stylist_id: Optional[int] = None
    created_at: datetime

    class Config:
        from_attributes = True

class BookingUpdate(BaseModel):
    """اسکیما برای بروزرسانی نوبت"""
    status: Optional[BookingStatus] = None
    notes: Optional[str] = Field(None, max_length=500)
    paid_amount: Optional[float] = Field(None, ge=0)
    payment_method: Optional[str] = None
    is_paid: Optional[bool] = None

class BookingResponse(BaseModel):
    """اسکیما پاسخ عمومی برای عملیات نوبت"""
    message: str
    booking_id: Optional[int] = None
    success: bool = True
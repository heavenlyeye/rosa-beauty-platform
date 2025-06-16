from pydantic import BaseModel, Field, validator
from typing import Optional
from enum import Enum

# تعریف محلی ServiceCategory
class ServiceCategory(str, Enum):
    HAIR_CUT = "hair_cut"              # کوتاهی مو
    HAIR_COLOR = "hair_color"          # رنگ مو
    FACIAL = "facial"                  # پاکسازی پوست
    MAKEUP = "makeup"                  # آرایش
    NAIL = "nail"                      # ناخن
    MASSAGE = "massage"                # ماساژ
    EYEBROW = "eyebrow"               # ابرو
    HAIR_TREATMENT = "hair_treatment"  # درمان مو
    SKIN_CARE = "skin_care"           # مراقبت پوست
    OTHER = "other"                   # سایر

class ServiceCreate(BaseModel):
    """اسکیما برای ایجاد خدمت جدید"""
    name: str = Field(..., min_length=2, max_length=100, description="نام خدمت")
    description: Optional[str] = Field(None, max_length=500, description="توضیحات خدمت")
    category: ServiceCategory = Field(..., description="دسته‌بندی خدمت")
    price: float = Field(..., gt=0, description="قیمت خدمت (تومان)")
    discount_price: Optional[float] = Field(None, ge=0, description="قیمت با تخفیف")
    duration_minutes: int = Field(60, ge=15, le=480, description="مدت زمان خدمت (دقیقه)")
    is_available: bool = Field(True, description="آیا خدمت فعال است؟")
    requires_appointment: bool = Field(True, description="آیا نیاز به نوبت دارد؟")

class ServiceUpdate(BaseModel):
    """اسکیما برای بروزرسانی خدمت"""
    name: Optional[str] = Field(None, min_length=2, max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    category: Optional[ServiceCategory] = None
    price: Optional[float] = Field(None, gt=0)
    discount_price: Optional[float] = Field(None, ge=0)
    duration_minutes: Optional[int] = Field(None, ge=15, le=480)
    is_available: Optional[bool] = None
    requires_appointment: Optional[bool] = None

class ServiceRead(BaseModel):
    """اسکیما برای خواندن خدمت"""
    id: int
    name: str
    description: Optional[str] = None
    category: ServiceCategory
    price: float
    discount_price: Optional[float] = None
    duration_minutes: int
    is_available: bool
    requires_appointment: bool
    salon_id: int

    class Config:
        from_attributes = True

class ServiceResponse(BaseModel):
    """اسکیما پاسخ عمومی برای عملیات خدمات"""
    message: str
    service_id: Optional[int] = None
    service_name: Optional[str] = None
    success: bool = True

# تعریف category names برای استفاده در API
SERVICE_CATEGORY_NAMES = {
    ServiceCategory.HAIR_CUT: "کوتاهی مو",
    ServiceCategory.HAIR_COLOR: "رنگ مو", 
    ServiceCategory.FACIAL: "پاکسازی پوست",
    ServiceCategory.MAKEUP: "آرایش",
    ServiceCategory.NAIL: "ناخن",
    ServiceCategory.MASSAGE: "ماساژ",
    ServiceCategory.EYEBROW: "ابرو",
    ServiceCategory.HAIR_TREATMENT: "درمان مو",
    ServiceCategory.SKIN_CARE: "مراقبت پوست",
    ServiceCategory.OTHER: "سایر"
}

def get_category_name(category: ServiceCategory) -> str:
    """تابع کمکی برای دریافت نام فارسی دسته‌بندی"""
    return SERVICE_CATEGORY_NAMES.get(category, "نامشخص")
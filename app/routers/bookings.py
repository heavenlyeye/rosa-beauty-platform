from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import and_, func, desc
from typing import List, Optional
from datetime import datetime, date
import logging

from ..database import get_db
from ..models.salon import BeautySalon
from ..schemas.booking import BookingCreateFromForm, BookingRead, BookingStatus
from ..auth.jwt_handler import get_current_user

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/api/bookings",
    tags=["bookings"],
    responses={404: {"description": "Not found"}}
)

@router.post("/", response_model=dict, status_code=status.HTTP_201_CREATED)
async def create_booking(
    booking_data: dict,
    current_user: BeautySalon = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """ایجاد نوبت جدید"""
    try:
        logger.info(f"Creating new booking for salon: {current_user.name}")
        
        # شبیه‌سازی ایجاد نوبت
        return {
            "message": "نوبت با موفقیت ثبت شد",
            "booking_id": 123,
            "customer_name": booking_data.get("customer_name", ""),
            "service_name": "خدمت نمونه",
            "booking_date": booking_data.get("booking_date", ""),
            "total_price": 150000
        }
        
    except Exception as e:
        logger.error(f"Error creating booking: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"خطا در ایجاد نوبت: {str(e)}"
        )

@router.get("/", response_model=List[dict])
async def get_bookings(
    current_user: BeautySalon = Depends(get_current_user),
    db: Session = Depends(get_db),
    date_from: Optional[date] = Query(None, description="از تاریخ"),
    date_to: Optional[date] = Query(None, description="تا تاریخ"),
    limit: int = Query(50, ge=1, le=100, description="تعداد نتایج")
):
    """دریافت لیست نوبت‌های سالن"""
    try:
        # شبیه‌سازی داده‌ها
        mock_bookings = [
            {
                "id": 1,
                "booking_date": "2024-01-15T10:30:00",
                "customer_name": "خانم احمدی",
                "customer_phone": "09121234567",
                "service_name": "رنگ مو",
                "service_price": 450000,
                "total_price": 450000,
                "paid_amount": 450000,
                "is_paid": True,
                "payment_method": "cash",
                "status": "completed",
                "status_text": "تکمیل شده",
                "notes": "",
                "created_at": "2024-01-15T09:00:00"
            },
            {
                "id": 2,
                "booking_date": "2024-01-15T12:00:00",
                "customer_name": "خانم محمدی",
                "customer_phone": "09129876543",
                "service_name": "کوتاهی مو",
                "service_price": 120000,
                "total_price": 120000,
                "paid_amount": 120000,
                "is_paid": True,
                "payment_method": "card",
                "status": "completed",
                "status_text": "تکمیل شده",
                "notes": "",
                "created_at": "2024-01-15T11:30:00"
            }
        ]
        
        return mock_bookings
        
    except Exception as e:
        logger.error(f"Error fetching bookings: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="خطا در دریافت نوبت‌ها"
        )

@router.get("/today", response_model=List[dict])
async def get_today_bookings(
    current_user: BeautySalon = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """دریافت نوبت‌های امروز"""
    try:
        # شبیه‌سازی نوبت‌های امروز
        today_bookings = [
            {
                "id": 1,
                "time": "09:00",
                "customer_name": "خانم احمدی",
                "service_name": "رنگ مو",
                "total_price": 450000,
                "status": "completed",
                "status_text": "تکمیل شده"
            },
            {
                "id": 2,
                "time": "10:30",
                "customer_name": "خانم محمدی",
                "service_name": "کوتاهی مو",
                "total_price": 120000,
                "status": "confirmed",
                "status_text": "تایید شده"
            },
            {
                "id": 3,
                "time": "12:00",
                "customer_name": "خانم رضایی",
                "service_name": "ماساژ صورت",
                "total_price": 200000,
                "status": "pending",
                "status_text": "در انتظار"
            }
        ]
        
        return today_bookings
        
    except Exception as e:
        logger.error(f"Error fetching today's bookings: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="خطا در دریافت نوبت‌های امروز"
        )

@router.get("/stats", response_model=dict)
async def get_booking_stats(
    current_user: BeautySalon = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """دریافت آمار نوبت‌ها"""
    try:
        # شبیه‌سازی آمار
        return {
            "today_appointments": 12,
            "pending_appointments": 3,
            "total_customers": 145,
            "monthly_revenue": 2500000
        }
        
    except Exception as e:
        logger.error(f"Error fetching booking stats: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="خطا در دریافت آمار"
        )

@router.get("/customers", response_model=List[dict])
async def get_salon_customers(
    current_user: BeautySalon = Depends(get_current_user),
    db: Session = Depends(get_db),
    search: Optional[str] = Query(None, description="جستجو در نام یا شماره تلفن"),
    filter_type: Optional[str] = Query("all", description="نوع فیلتر: all, active, new")
):
    """دریافت لیست مشتریان سالن"""
    try:
        # شبیه‌سازی داده‌های مشتریان
        mock_customers = [
            {
                "id": 1,
                "name": "خانم احمدی",
                "phone": "09121234567",
                "total_visits": 12,
                "last_visit": "1403/03/15",
                "total_spent": 2400000,
                "is_active": True
            },
            {
                "id": 2,
                "name": "خانم محمدی",
                "phone": "09129876543",
                "total_visits": 8,
                "last_visit": "1403/03/10",
                "total_spent": 1600000,
                "is_active": True
            },
            {
                "id": 3,
                "name": "خانم رضایی",
                "phone": "09125555555",
                "total_visits": 15,
                "last_visit": "1403/03/12",
                "total_spent": 3200000,
                "is_active": True
            }
        ]
        
        # اعمال فیلتر جستجو
        if search:
            search_lower = search.lower()
            mock_customers = [
                c for c in mock_customers 
                if search_lower in c["name"].lower() or search in c["phone"]
            ]
        
        # اعمال فیلتر نوع
        if filter_type == "active":
            mock_customers = [c for c in mock_customers if c["total_visits"] > 5]
        elif filter_type == "new":
            mock_customers = [c for c in mock_customers if c["total_visits"] <= 3]
        
        return mock_customers
        
    except Exception as e:
        logger.error(f"Error fetching customers: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="خطا در دریافت مشتریان"
        )

@router.put("/{booking_id}/status", response_model=dict)
async def update_booking_status(
    booking_id: int,
    new_status: BookingStatus,
    current_user: BeautySalon = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """بروزرسانی وضعیت نوبت"""
    try:
        # شبیه‌سازی بروزرسانی وضعیت
        logger.info(f"Booking {booking_id} status updated to {new_status}")
        
        return {
            "message": "وضعیت نوبت بروزرسانی شد",
            "booking_id": booking_id,
            "new_status": new_status.value
        }
        
    except Exception as e:
        logger.error(f"Error updating booking status: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="خطا در بروزرسانی وضعیت"
        )

@router.delete("/{booking_id}", response_model=dict)
async def cancel_booking(
    booking_id: int,
    current_user: BeautySalon = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """لغو نوبت"""
    try:
        # شبیه‌سازی لغو نوبت
        logger.info(f"Booking {booking_id} cancelled by salon {current_user.name}")
        
        return {
            "message": "نوبت با موفقیت لغو شد",
            "booking_id": booking_id
        }
        
    except Exception as e:
        logger.error(f"Error cancelling booking: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="خطا در لغو نوبت"
        )

def get_status_text(status: BookingStatus) -> str:
    """تبدیل وضعیت به متن فارسی"""
    status_map = {
        BookingStatus.PENDING: "در انتظار تایید",
        BookingStatus.CONFIRMED: "تایید شده",
        BookingStatus.IN_PROGRESS: "در حال انجام",
        BookingStatus.COMPLETED: "تکمیل شده",
        BookingStatus.CANCELLED: "لغو شده",
        BookingStatus.NO_SHOW: "عدم حضور"
    }
    return status_map.get(status, "نامشخص")
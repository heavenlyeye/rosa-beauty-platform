from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
import logging

from ..database import get_db
from ..models.salon import BeautySalon
from ..schemas.service import ServiceCategory, get_category_name
from ..auth.jwt_handler import get_current_user

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/api/services",
    tags=["services"],
    responses={404: {"description": "Not found"}}
)

@router.get("/", response_model=List[dict])
async def get_services(
    current_user: BeautySalon = Depends(get_current_user),
    db: Session = Depends(get_db),
    category: Optional[ServiceCategory] = Query(None, description="فیلتر دسته‌بندی"),
    search: Optional[str] = Query(None, description="جستجو در نام خدمت")
):
    """دریافت لیست خدمات سالن با امکان فیلتر"""
    try:
        # شبیه‌سازی داده‌های خدمات
        mock_services = [
            {
                "id": 1,
                "name": "کوتاهی مو",
                "description": "کوتاهی مو با استایل‌های مختلف",
                "category": "hair_cut",
                "category_name": "کوتاهی مو",
                "price": 150000,
                "discount_price": None,
                "duration_minutes": 60,
                "is_available": True,
                "requires_appointment": True,
                "booking_count": 15,
                "popularity_rank": 85.5
            },
            {
                "id": 2,
                "name": "رنگ مو",
                "description": "رنگ مو با رنگ‌های مختلف",
                "category": "hair_color",
                "category_name": "رنگ مو",
                "price": 450000,
                "discount_price": 400000,
                "duration_minutes": 120,
                "is_available": True,
                "requires_appointment": True,
                "booking_count": 8,
                "popularity_rank": 78.2
            },
            {
                "id": 3,
                "name": "پاکسازی پوست",
                "description": "پاکسازی عمیق پوست صورت",
                "category": "facial",
                "category_name": "پاکسازی پوست",
                "price": 200000,
                "discount_price": None,
                "duration_minutes": 90,
                "is_available": True,
                "requires_appointment": True,
                "booking_count": 12,
                "popularity_rank": 82.1
            },
            {
                "id": 4,
                "name": "آرایش عروس",
                "description": "آرایش مخصوص عروس",
                "category": "makeup",
                "category_name": "آرایش",
                "price": 800000,
                "discount_price": None,
                "duration_minutes": 180,
                "is_available": True,
                "requires_appointment": True,
                "booking_count": 3,
                "popularity_rank": 65.0
            }
        ]
        
        # اعمال فیلتر دسته‌بندی
        if category:
            mock_services = [s for s in mock_services if s["category"] == category.value]
        
        # اعمال فیلتر جستجو
        if search:
            search_lower = search.lower()
            mock_services = [s for s in mock_services if search_lower in s["name"].lower()]
        
        # مرتب‌سازی بر اساس محبوبیت
        mock_services.sort(key=lambda x: x["popularity_rank"], reverse=True)
        
        return mock_services
        
    except Exception as e:
        logger.error(f"Error fetching services: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="خطا در دریافت خدمات"
        )

@router.get("/categories", response_model=List[dict])
async def get_service_categories():
    """دریافت لیست دسته‌بندی‌های خدمات"""
    categories = [
        {"value": "hair_cut", "label": "کوتاهی مو", "icon": "fas fa-cut"},
        {"value": "hair_color", "label": "رنگ مو", "icon": "fas fa-palette"},
        {"value": "facial", "label": "پاکسازی پوست", "icon": "fas fa-spa"},
        {"value": "makeup", "label": "آرایش", "icon": "fas fa-magic"},
        {"value": "nail", "label": "ناخن", "icon": "fas fa-hand-sparkles"},
        {"value": "massage", "label": "ماساژ", "icon": "fas fa-hands"},
        {"value": "eyebrow", "label": "ابرو", "icon": "fas fa-eye"},
        {"value": "hair_treatment", "label": "درمان مو", "icon": "fas fa-prescription-bottle"},
        {"value": "skin_care", "label": "مراقبت پوست", "icon": "fas fa-heart"},
        {"value": "other", "label": "سایر", "icon": "fas fa-ellipsis-h"}
    ]
    return categories

@router.get("/popular", response_model=List[dict])
async def get_popular_services(
    current_user: BeautySalon = Depends(get_current_user),
    db: Session = Depends(get_db),
    limit: int = Query(5, ge=1, le=20, description="تعداد خدمات محبوب")
):
    """دریافت محبوب‌ترین خدمات بر اساس تعداد رزرو"""
    try:
        # شبیه‌سازی خدمات محبوب
        popular_services = [
            {
                "id": 1,
                "name": "کوتاهی مو",
                "category": "hair_cut",
                "category_name": "کوتاهی مو",
                "price": 150000,
                "booking_count": 15,
                "total_revenue": 2250000,
                "average_price": 150000,
                "popularity_score": 85.5
            },
            {
                "id": 3,
                "name": "پاکسازی پوست",
                "category": "facial",
                "category_name": "پاکسازی پوست",
                "price": 200000,
                "booking_count": 12,
                "total_revenue": 2400000,
                "average_price": 200000,
                "popularity_score": 82.1
            },
            {
                "id": 2,
                "name": "رنگ مو",
                "category": "hair_color",
                "category_name": "رنگ مو",
                "price": 450000,
                "booking_count": 8,
                "total_revenue": 3600000,
                "average_price": 450000,
                "popularity_score": 78.2
            }
        ]
        
        return popular_services[:limit]
        
    except Exception as e:
        logger.error(f"Error fetching popular services: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="خطا در دریافت خدمات محبوب"
        )

@router.get("/stats", response_model=dict)
async def get_service_stats(
    current_user: BeautySalon = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """دریافت آمار کلی خدمات"""
    try:
        # شبیه‌سازی آمار خدمات
        return {
            "total_services": 4,
            "active_services": 4,
            "inactive_services": 0,
            "average_price": 350000,
            "best_seller": "کوتاهی مو",
            "best_seller_bookings": 15,
            "category_breakdown": [
                {
                    "category": "hair_cut",
                    "category_name": "کوتاهی مو",
                    "service_count": 1,
                    "average_price": 150000
                },
                {
                    "category": "hair_color",
                    "category_name": "رنگ مو",
                    "service_count": 1,
                    "average_price": 450000
                },
                {
                    "category": "facial",
                    "category_name": "پاکسازی پوست",
                    "service_count": 1,
                    "average_price": 200000
                },
                {
                    "category": "makeup",
                    "category_name": "آرایش",
                    "service_count": 1,
                    "average_price": 800000
                }
            ]
        }
        
    except Exception as e:
        logger.error(f"Error fetching service stats: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="خطا در دریافت آمار خدمات"
        )

@router.post("/", response_model=dict, status_code=status.HTTP_201_CREATED)
async def create_service(
    service_data: dict,
    current_user: BeautySalon = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """ایجاد خدمت جدید"""
    try:
        # شبیه‌سازی ایجاد خدمت
        return {
            "message": "خدمت با موفقیت ایجاد شد",
            "service_id": 5,
            "service_name": service_data.get("name", "خدمت جدید"),
            "category": service_data.get("category", "other"),
            "price": service_data.get("price", 0)
        }
        
    except Exception as e:
        logger.error(f"Error creating service: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"خطا در ایجاد خدمت: {str(e)}"
        )
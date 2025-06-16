from fastapi import APIRouter, Depends, HTTPException, Query, Response
from sqlalchemy.orm import Session
from typing import Optional, Dict, Any
from datetime import date
import logging

from ..database import get_db
from ..models.salon import BeautySalon
from ..auth.jwt_handler import get_current_user

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/api/reports",
    tags=["reports"],
    responses={404: {"description": "Not found"}}
)

@router.get("/sales", response_model=Dict[str, Any])
async def get_sales_report(
    current_user: BeautySalon = Depends(get_current_user),
    db: Session = Depends(get_db),
    date_from: Optional[date] = Query(None, description="از تاریخ"),
    date_to: Optional[date] = Query(None, description="تا تاریخ")
):
    """گزارش فروش و درآمد"""
    try:
        # شبیه‌سازی گزارش فروش
        return {
            "period": f"{date_from or '1403/01/01'} تا {date_to or '1403/03/15'}",
            "summary": {
                "total_sales": 2500000,
                "total_revenue": 2800000,
                "total_bookings": 25,
                "completed_bookings": 20,
                "cancelled_bookings": 3,
                "pending_bookings": 2,
                "completion_rate": 80.0,
                "average_sale": 125000
            },
            "daily_sales": [
                {"date": "1403/03/13", "sales": 450000, "bookings": 3},
                {"date": "1403/03/14", "sales": 320000, "bookings": 2},
                {"date": "1403/03/15", "sales": 680000, "bookings": 4}
            ],
            "popular_services": [
                {
                    "service_id": 1,
                    "name": "کوتاهی مو",
                    "category": "hair_cut",
                    "booking_count": 8,
                    "total_revenue": 1200000,
                    "average_revenue": 150000
                },
                {
                    "service_id": 2,
                    "name": "رنگ مو",
                    "category": "hair_color",
                    "booking_count": 5,
                    "total_revenue": 2250000,
                    "average_revenue": 450000
                }
            ],
            "trends": {
                "trend": "increasing",
                "change_percentage": 15.2,
                "first_period_avg": 120000,
                "second_period_avg": 138000
            }
        }
        
    except Exception as e:
        logger.error(f"Error generating sales report: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="خطا در تولید گزارش فروش"
        )

@router.get("/customers", response_model=Dict[str, Any])
async def get_customers_report(
    current_user: BeautySalon = Depends(get_current_user),
    db: Session = Depends(get_db),
    date_from: Optional[date] = Query(None, description="از تاریخ"),
    date_to: Optional[date] = Query(None, description="تا تاریخ")
):
    """گزارش مشتریان و رفتار آنها"""
    try:
        # شبیه‌سازی گزارش مشتریان
        return {
            "period": f"{date_from or '1403/01/01'} تا {date_to or '1403/03/15'}",
            "summary": {
                "total_customers": 150,
                "active_customers": 45,
                "new_customers": 12,
                "repeat_customers": 103,
                "retention_rate": 68.7
            },
            "top_customers": [
                {
                    "customer_id": 1,
                    "name": "خانم احمدی",
                    "phone": "09121234567",
                    "visit_count": 12,
                    "total_spent": 2400000,
                    "average_per_visit": 200000,
                    "last_visit": "1403/03/15",
                    "loyalty_score": 85.5
                },
                {
                    "customer_id": 2,
                    "name": "خانم رضایی",
                    "phone": "09125555555",
                    "visit_count": 15,
                    "total_spent": 3200000,
                    "average_per_visit": 213333,
                    "last_visit": "1403/03/12",
                    "loyalty_score": 92.1
                }
            ],
            "customer_segments": {
                "new_customers": {"count": 25, "percentage": 16.7},
                "regular_customers": {"count": 82, "percentage": 54.7},
                "loyal_customers": {"count": 35, "percentage": 23.3},
                "vip_customers": {"count": 8, "percentage": 5.3}
            },
            "retention_analysis": {
                "previous_period_customers": 128,
                "current_period_customers": 150,
                "returning_customers": 103,
                "retention_rate": 80.5,
                "new_customers_current_period": 47
            }
        }
        
    except Exception as e:
        logger.error(f"Error generating customers report: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="خطا در تولید گزارش مشتریان"
        )

@router.get("/services", response_model=Dict[str, Any])
async def get_services_report(
    current_user: BeautySalon = Depends(get_current_user),
    db: Session = Depends(get_db),
    date_from: Optional[date] = Query(None, description="از تاریخ"),
    date_to: Optional[date] = Query(None, description="تا تاریخ")
):
    """گزارش عملکرد خدمات"""
    try:
        # شبیه‌سازی گزارش خدمات
        return {
            "period": f"{date_from or '1403/01/01'} تا {date_to or '1403/03/15'}",
            "summary": {
                "total_services": 4,
                "active_services": 4,
                "inactive_services": 0,
                "services_with_bookings": 4
            },
            "service_performance": [
                {
                    "service_id": 1,
                    "name": "کوتاهی مو",
                    "category": "hair_cut",
                    "category_name": "کوتاهی مو",
                    "base_price": 150000,
                    "booking_count": 15,
                    "total_revenue": 2250000,
                    "average_revenue": 150000,
                    "performance_score": 85.5
                },
                {
                    "service_id": 2,
                    "name": "رنگ مو",
                    "category": "hair_color",
                    "category_name": "رنگ مو",
                    "base_price": 450000,
                    "booking_count": 8,
                    "total_revenue": 3600000,
                    "average_revenue": 450000,
                    "performance_score": 78.2
                },
                {
                    "service_id": 3,
                    "name": "پاکسازی پوست",
                    "category": "facial",
                    "category_name": "پاکسازی پوست",
                    "base_price": 200000,
                    "booking_count": 12,
                    "total_revenue": 2400000,
                    "average_revenue": 200000,
                    "performance_score": 82.1
                }
            ],
            "category_analysis": [
                {
                    "category": "hair_cut",
                    "category_name": "کوتاهی مو",
                    "total_bookings": 15,
                    "total_revenue": 2250000,
                    "average_price": 150000,
                    "market_share": 28.5
                },
                {
                    "category": "hair_color",
                    "category_name": "رنگ مو",
                    "total_bookings": 8,
                    "total_revenue": 3600000,
                    "average_price": 450000,
                    "market_share": 45.6
                }
            ],
            "recommendations": [
                "خدمت کوتاهی مو محبوب‌ترین خدمت شما است.",
                "خدمات رنگ مو درآمد بالایی دارند.",
                "تمرکز بر تبلیغات خدمات پرسود توصیه می‌شود."
            ]
        }
        
    except Exception as e:
        logger.error(f"Error generating services report: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="خطا در تولید گزارش خدمات"
        )

@router.get("/financial", response_model=Dict[str, Any])
async def get_financial_report(
    current_user: BeautySalon = Depends(get_current_user),
    db: Session = Depends(get_db),
    date_from: Optional[date] = Query(None, description="از تاریخ"),
    date_to: Optional[date] = Query(None, description="تا تاریخ")
):
    """گزارش مالی تفصیلی"""
    try:
        # شبیه‌سازی گزارش مالی
        return {
            "period": f"{date_from or '1403/01/01'} تا {date_to or '1403/03/15'}",
            "revenue_summary": {
                "total_revenue": 2800000,
                "actual_received": 2500000,
                "outstanding_amount": 300000,
                "collection_rate": 89.3
            },
            "payment_breakdown": [
                {
                    "method": "cash",
                    "method_name": "نقدی",
                    "transaction_count": 15,
                    "total_amount": 1500000
                },
                {
                    "method": "card",
                    "method_name": "کارت",
                    "transaction_count": 8,
                    "total_amount": 800000
                },
                {
                    "method": "online",
                    "method_name": "آنلاین",
                    "transaction_count": 2,
                    "total_amount": 200000
                }
            ],
            "daily_cashflow": [
                {
                    "date": "1403/03/13",
                    "inflow": 450000,
                    "outflow": 0,
                    "net_cashflow": 450000,
                    "transaction_count": 3
                },
                {
                    "date": "1403/03/14",
                    "inflow": 320000,
                    "outflow": 0,
                    "net_cashflow": 320000,
                    "transaction_count": 2
                },
                {
                    "date": "1403/03/15",
                    "inflow": 680000,
                    "outflow": 0,
                    "net_cashflow": 680000,
                    "transaction_count": 4
                }
            ],
            "period_comparison": {
                "current_period_revenue": 2500000,
                "previous_period_revenue": 2200000,
                "revenue_change": 300000,
                "revenue_change_percentage": 13.6,
                "trend": "up"
            },
            "financial_kpis": {
                "revenue_per_day": 83333,
                "collection_efficiency": 89.3,
                "outstanding_ratio": 10.7,
                "cash_conversion_rate": 89.3
            }
        }
        
    except Exception as e:
        logger.error(f"Error generating financial report: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="خطا در تولید گزارش مالی"
        )

@router.get("/export/csv")
async def export_report_csv(
    report_type: str = Query(..., description="نوع گزارش: sales, customers, services, financial"),
    current_user: BeautySalon = Depends(get_current_user),
    db: Session = Depends(get_db),
    date_from: Optional[date] = Query(None),
    date_to: Optional[date] = Query(None)
):
    """خروجی گزارش به فرمت CSV"""
    try:
        # شبیه‌سازی تولید CSV
        csv_content = f"""گزارش {report_type} سالن زیبایی Rosa
تاریخ تولید گزارش: 1403/03/15
دوره گزارش: {date_from or '1403/01/01'} تا {date_to or '1403/03/15'}

نوع,تاریخ,زمان,مشتری,تلفن,خدمت,مبلغ,پرداخت شده,وضعیت,یادداشت
نوبت,1403/03/15,09:00,خانم احمدی,09121234567,رنگ مو,450000,450000,تکمیل شده,
نوبت,1403/03/15,10:30,خانم محمدی,09129876543,کوتاهی مو,120000,120000,تکمیل شده,
نوبت,1403/03/16,11:00,خانم رضایی,09125555555,پاکسازی پوست,200000,100000,در انتظار,پرداخت ناقص"""
        
        filename = f"rosa-{report_type}-{date.today()}.csv"
        
        # ایجاد Response با محتوای CSV
        response = Response(
            content=csv_content,
            media_type="text/csv; charset=utf-8",
            headers={
                "Content-Disposition": f"attachment; filename={filename}",
                "Content-Type": "text/csv; charset=utf-8"
            }
        )
        
        logger.info(f"CSV export generated for {report_type} report by salon {current_user.name}")
        return response
        
    except Exception as e:
        logger.error(f"Error exporting CSV: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="خطا در تولید خروجی CSV"
        )

@router.get("/performance")
async def get_performance_report(
    current_user: BeautySalon = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """گزارش عملکرد کلی"""
    try:
        return {
            "period": "month",
            "sales": {"total_sales": 2500000},
            "customers": {"active_customers": 45},
            "services": {
                "popular_services": [
                    {"name": "کوتاهی مو", "booking_count": 15}
                ]
            },
            "overall_score": 85.2,
            "recommendations": [
                "عملکرد سالن در حد مطلوب است",
                "تمرکز بر جذب مشتریان جدید توصیه می‌شود"
            ]
        }
        
    except Exception as e:
        logger.error(f"Error generating performance report: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="خطا در تولید گزارش عملکرد"
        )
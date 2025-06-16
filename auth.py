from fastapi import APIRouter
router = APIRouter(prefix="/api/customers", tags=["customers"])

@router.get("/")
async def get_customers():
    return [{"id": 1, "full_name": "نمونه مشتری", "phone": "09123456789"}]

@router.get("/search")
async def search_customers():
    return [{"id": 1, "full_name": "نمونه مشتری", "phone": "09123456789"}]

from sqlalchemy.orm import Session
from sqlalchemy import and_
from typing import List, Optional
from ..models.service import Service, ServiceCategory
from ..schemas.service import ServiceCreate, ServiceRead

class ServiceService:
   def __init__(self, db: Session):
       self.db = db
   
   def get_categories(self) -> List[dict]:
       """دریافت لیست دسته‌بندی‌ها"""
       categories = [
           {"value": "hair_cut", "label": "کوتاهی مو"},
           {"value": "hair_color", "label": "رنگ مو"},
           {"value": "facial", "label": "پاکسازی پوست"},
           {"value": "makeup", "label": "آرایش"},
           {"value": "nail", "label": "ناخن"},
           {"value": "massage", "label": "ماساژ"},
           {"value": "eyebrow", "label": "ابرو"},
           {"value": "hair_treatment", "label": "درمان مو"},
           {"value": "skin_care", "label": "مراقبت پوست"},
           {"value": "other", "label": "سایر"}
       ]
       return categories

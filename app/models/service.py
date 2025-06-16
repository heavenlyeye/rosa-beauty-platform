from sqlalchemy import Column, Integer, String, Text, Float, Boolean, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import relationship
from enum import Enum as PyEnum
from ..database import Base

class ServiceCategory(PyEnum):
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

class Service(Base):
    __tablename__ = "services"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, index=True)
    description = Column(Text, nullable=True)
    category = Column(SQLEnum(ServiceCategory), nullable=False, index=True)
    price = Column(Float, nullable=False)
    discount_price = Column(Float, nullable=True)
    duration_minutes = Column(Integer, nullable=False, default=60)
    is_available = Column(Boolean, default=True)
    requires_appointment = Column(Boolean, default=True)
    salon_id = Column(Integer, ForeignKey("beauty_salons.id"), nullable=False)
    
    def __repr__(self):
        return f"<Service(id={self.id}, name='{self.name}', price={self.price})>"
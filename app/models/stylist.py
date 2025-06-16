from sqlalchemy import Column, Integer, String, Text, Boolean, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from ..database import Base

class Stylist(Base):
    __tablename__ = "stylists"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    bio = Column(Text, nullable=True)
    phone = Column(String(20), nullable=True)
    experience_years = Column(Integer, default=0)
    specialties = Column(Text, nullable=True)
    is_available = Column(Boolean, default=True)
    average_rating = Column(Float, default=0.0)
    total_ratings = Column(Integer, default=0)
    salon_id = Column(Integer, ForeignKey("beauty_salons.id"), nullable=False)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    def __repr__(self):
        return f"<Stylist(id={self.id}, name='{self.name}')>"
from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, Float
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from ..database import Base

class BeautySalon(Base):
    __tablename__ = "beauty_salons"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    name = Column(String(100), nullable=False, index=True)
    address = Column(Text, nullable=True)
    phone = Column(String(20), nullable=True)
    instagram = Column(String(100), nullable=True)
    description = Column(Text, nullable=True)
    
    # Business Info
    is_verified = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    
    # Location
    city = Column(String(50), nullable=True)
    province = Column(String(50), nullable=True)
    
    # Ratings
    average_rating = Column(Float, default=0.0)
    total_ratings = Column(Integer, default=0)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    def __repr__(self):
        return f"<BeautySalon(id={self.id}, name='{self.name}')>"
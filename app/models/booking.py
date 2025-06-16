from sqlalchemy import Column, Integer, String, DateTime, Text, Float, Boolean, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from enum import Enum as PyEnum
from ..database import Base

class BookingStatus(PyEnum):
    PENDING = "pending"        # در انتظار تایید
    CONFIRMED = "confirmed"    # تایید شده
    IN_PROGRESS = "in_progress"  # در حال انجام
    COMPLETED = "completed"    # تکمیل شده
    CANCELLED = "cancelled"    # لغو شده
    NO_SHOW = "no_show"       # عدم حضور

class Booking(Base):
    __tablename__ = "bookings"
    
    id = Column(Integer, primary_key=True, index=True)
    booking_date = Column(DateTime(timezone=True), nullable=False, index=True)
    status = Column(SQLEnum(BookingStatus), default=BookingStatus.PENDING, nullable=False)
    notes = Column(Text, nullable=True)
    total_price = Column(Float, nullable=False)
    paid_amount = Column(Float, default=0.0)
    is_paid = Column(Boolean, default=False)
    payment_method = Column(String(50), nullable=True)
    
    # Foreign Keys
    customer_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    salon_id = Column(Integer, ForeignKey("beauty_salons.id"), nullable=False)
    service_id = Column(Integer, ForeignKey("services.id"), nullable=False)
    stylist_id = Column(Integer, ForeignKey("stylists.id"), nullable=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    completed_at = Column(DateTime(timezone=True), nullable=True)
    
    def __repr__(self):
        return f"<Booking(id={self.id}, status='{self.status}', date={self.booking_date})>"
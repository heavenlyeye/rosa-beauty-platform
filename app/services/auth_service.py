from sqlalchemy.orm import Session
from sqlalchemy import and_, or_
from typing import List, Optional
from ..models.user import User, UserRole
from ..schemas.user import UserCreate, UserRead
from ..auth.jwt_handler import hash_password

class AuthService:
    def __init__(self, db: Session):
        self.db = db
    
    def create_customer(self, customer_data: UserCreate) -> User:
        """ایجاد مشتری جدید"""
        
        # بررسی وجود نام کاربری یا ایمیل
        existing = self.db.query(User).filter(
            or_(
                User.username == customer_data.username,
                User.email == customer_data.email
            )
        ).first()
        
        if existing:
            if existing.username == customer_data.username:
                raise ValueError("این نام کاربری قبلاً ثبت شده است")
            if existing.email == customer_data.email:
                raise ValueError("این ایمیل قبلاً ثبت شده است")
        
        # ایجاد مشتری جدید
        hashed_password = hash_password(customer_data.password)
        db_user = User(
            username=customer_data.username,
            email=customer_data.email,
            hashed_password=hashed_password,
            full_name=customer_data.full_name,
            phone=customer_data.phone,
            role=UserRole.CLIENT,
            is_active=True,
            is_verified=False
        )
        
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        return db_user
    
    def get_customers(self, skip: int = 0, limit: int = 100, search: str = None) -> List[User]:
        """دریافت لیست مشتریان"""
        query = self.db.query(User).filter(User.role == UserRole.CLIENT)
        
        if search:
            search_filter = or_(
                User.full_name.ilike(f"%{search}%"),
                User.username.ilike(f"%{search}%"),
                User.phone.ilike(f"%{search}%"),
                User.email.ilike(f"%{search}%")
            )
            query = query.filter(search_filter)
        
        return query.offset(skip).limit(limit).all()
    
    def get_customer_by_id(self, customer_id: int) -> Optional[User]:
        """دریافت مشتری با ID"""
        return self.db.query(User).filter(
            and_(User.id == customer_id, User.role == UserRole.CLIENT)
        ).first()
    
    def search_customers(self, query: str) -> List[User]:
        """جستجوی مشتریان"""
        if not query or len(query) < 2:
            return []
        
        search_filter = or_(
            User.full_name.ilike(f"%{query}%"),
            User.username.ilike(f"%{query}%"),
            User.phone.ilike(f"%{query}%")
        )
        
        return self.db.query(User).filter(
            and_(User.role == UserRole.CLIENT, search_filter)
        ).limit(10).all()
    
    def update_customer(self, customer_id: int, customer_data: dict) -> Optional[User]:
        """بروزرسانی اطلاعات مشتری"""
        customer = self.get_customer_by_id(customer_id)
        if not customer:
            return None
        
        for field, value in customer_data.items():
            if hasattr(customer, field) and value is not None:
                setattr(customer, field, value)
        
        self.db.commit()
        self.db.refresh(customer)
        return customer
    
    def delete_customer(self, customer_id: int) -> bool:
        """حذف مشتری (غیرفعال کردن)"""
        customer = self.get_customer_by_id(customer_id)
        if not customer:
            return False
        
        customer.is_active = False
        self.db.commit()
        return True
"""
🌹 Rosa Beauty Salon Platform
FastAPI Main Application with Multi-language Support
ترکیب کدهای موجود با ساختار جدید
"""

from fastapi import FastAPI, Depends, HTTPException, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.security import OAuth2PasswordRequestForm, HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from datetime import datetime
import jwt
import os
from typing import Optional, Dict, Any
import logging
from pathlib import Path

# Internal imports
from .config import settings
from .database import get_db, create_tables, engine
from .models.salon import BeautySalon
from .schemas.salon import SalonCreate
from .auth.jwt_handler import hash_password, verify_password, create_access_token

# Configure logging
logging.basicConfig(
    level=getattr(logging, settings.log_level),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="🌹 Rosa Beauty Salon Platform",
    description="سیستم هوشمند مدیریت سالن‌های زیبایی - Smart Beauty Salon Management System",
    version="2.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

# Security
security = HTTPBearer(auto_error=False)

# Mount static files
static_path = Path(__file__).parent / "static"
if static_path.exists():
    app.mount("/static", StaticFiles(directory=str(static_path)), name="static")
    logger.info(f"✅ Static files mounted from: {static_path}")

# Utility functions
def get_client_ip(request: Request) -> str:
    """Get client IP address"""
    return request.client.host if request.client else "unknown"

def log_security_event(event: str, ip: str, user: str = None, details: str = None):
    """Log security events"""
    logger.info(f"SECURITY_EVENT: {event} | IP: {ip} | User: {user} | Details: {details}")

def get_html_file(filename: str) -> str:
    """Helper function to read HTML files from static folder"""
    filepath = static_path / filename
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        logger.error(f"File not found: {filepath}")
        raise HTTPException(status_code=404, detail="صفحه یافت نشد")
    except Exception as e:
        logger.error(f"Error reading file: {str(e)}")
        raise HTTPException(status_code=500, detail="خطا در بارگذاری صفحه")

# Authentication dependencies
async def get_current_user(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security),
    session: Session = Depends(get_db)
) -> BeautySalon:
    """Get current authenticated user"""
    if not credentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    try:
        payload = jwt.decode(credentials.credentials, settings.secret_key, algorithms=[settings.algorithm])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token expired",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except jwt.JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # استفاده از query به جای session.exec
    user = session.query(BeautySalon).filter(BeautySalon.username == username).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return user

async def get_admin_user(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security)
) -> Dict[str, Any]:
    """Verify admin authentication"""
    if not credentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Admin authentication required",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    try:
        payload = jwt.decode(credentials.credentials, settings.secret_key, algorithms=[settings.algorithm])
        role = payload.get("role")
        is_admin = payload.get("is_admin", False)
        
        if role != "admin" or not is_admin:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Admin access required"
            )
        
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Admin token expired",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except jwt.JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid admin token",
            headers={"WWW-Authenticate": "Bearer"},
        )

# HTML Routes
@app.get("/", response_class=HTMLResponse)
async def read_root():
    """Serve main page"""
    try:
        html_file = static_path / "index.html"
        if html_file.exists():
            return FileResponse(html_file)
        else:
            return HTMLResponse("""
            <!DOCTYPE html>
            <html lang="fa" dir="rtl">
            <head>
                <meta charset="UTF-8">
                <title>🌹 Rosa Beauty Platform</title>
                <style>
                    body { font-family: 'Segoe UI', Tahoma, sans-serif; 
                           background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                           margin: 0; padding: 50px; text-align: center; color: white; }
                    .container { max-width: 600px; margin: 0 auto; }
                    h1 { font-size: 3rem; margin-bottom: 20px; }
                    p { font-size: 1.2rem; opacity: 0.9; }
                    .links { margin-top: 30px; }
                    .links a { background: rgba(255,255,255,0.2); color: white; 
                              padding: 15px 30px; text-decoration: none; 
                              border-radius: 25px; margin: 10px; display: inline-block; }
                </style>
            </head>
            <body>
                <div class="container">
                    <h1>🌹 Rosa Beauty Platform</h1>
                    <p>پلتفرم هوشمند مدیریت سالن‌های زیبایی</p>
                    <div class="links">
                        <a href="/api/docs">📖 API Documentation</a>
                        <a href="/dashboard">📊 Dashboard</a>
                        <a href="/admin">👑 Admin Panel</a>
                    </div>
                </div>
            </body>
            </html>
            """)
    except Exception as e:
        logger.error(f"Error serving root page: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard():
    """Serve dashboard page"""
    try:
        html_file = static_path / "dashboard.html"
        if html_file.exists():
            return FileResponse(html_file)
        else:
            return HTMLResponse("<h1>Dashboard page not found</h1>")
    except Exception as e:
        logger.error(f"Error serving dashboard: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.get("/admin", response_class=HTMLResponse)
async def admin_panel():
    """Serve admin panel"""
    try:
        html_file = static_path / "admin.html"
        if html_file.exists():
            return FileResponse(html_file)
        else:
            return HTMLResponse("<h1>Admin panel not found</h1>")
    except Exception as e:
        logger.error(f"Error serving admin panel: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

# API Routes
@app.get("/health")
async def health_check():
    """Health check endpoint"""
    try:
        # Test database connection
        with engine.connect() as conn:
            conn.execute("SELECT 1")
        
        return {
            "status": "healthy",
            "service": "Rosa Beauty Platform",
            "version": "2.0.0",
            "environment": settings.environment,
            "database": "connected",
            "timestamp": datetime.utcnow().isoformat()
        }
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return {
            "status": "unhealthy",
            "error": str(e)
        }

@app.post("/register")
async def register(
    salon: SalonCreate, 
    request: Request,
    session: Session = Depends(get_db)
):
    """Register new beauty salon"""
    client_ip = get_client_ip(request)
    
    try:
        logger.info(f"Registration attempt for username: {salon.username} from IP: {client_ip}")
        
        # بررسی وجود نام کاربری با استفاده از SQLAlchemy query
        existing = session.query(BeautySalon).filter(BeautySalon.username == salon.username).first()
        if existing:
            log_security_event("registration_failed", client_ip, salon.username, "Username already exists")
            raise HTTPException(status_code=400, detail="این نام کاربری قبلاً ثبت شده.")
        
        # Password validation
        if len(salon.password) < 6:
            raise HTTPException(status_code=400, detail="رمز عبور باید حداقل 6 کاراکتر باشد.")
        
        # Create new salon
        hashed_password = hash_password(salon.password)
        db_salon = BeautySalon(
            username=salon.username,
            hashed_password=hashed_password,
            name=salon.name,
            address=salon.address,
            phone=salon.phone,
            instagram=salon.instagram,
            description=salon.description
        )
        session.add(db_salon)
        session.commit()
        session.refresh(db_salon)
        
        log_security_event("registration_success", client_ip, salon.username, f"Salon: {salon.name}")
        logger.info(f"Successfully registered salon: {db_salon.name} with ID: {db_salon.id}")
        
        return {"message": "ثبت‌نام با موفقیت انجام شد.", "salon_id": db_salon.id}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Registration error: {str(e)}")
        log_security_event("registration_error", client_ip, salon.username, str(e))
        raise HTTPException(status_code=500, detail=f"خطا در ثبت‌نام: {str(e)}")

@app.post("/login")
async def login(
    request: Request,
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: Session = Depends(get_db)
):
    """User authentication"""
    client_ip = get_client_ip(request)
    
    try:
        logger.info(f"Login attempt for username: {form_data.username} from IP: {client_ip}")
        
        # استفاده از SQLAlchemy query به جای session.exec
        salon = session.query(BeautySalon).filter(BeautySalon.username == form_data.username).first()
        if not salon or not verify_password(form_data.password, salon.hashed_password):
            log_security_event("login_failed", client_ip, form_data.username, "Invalid credentials")
            raise HTTPException(status_code=401, detail="نام کاربری یا رمز اشتباه است.")
        
        token = create_access_token({"sub": salon.username})
        log_security_event("login_success", client_ip, form_data.username)
        logger.info(f"Successful login for username: {form_data.username}")
        
        return {"access_token": token, "token_type": "bearer"}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Login error: {str(e)}")
        log_security_event("login_error", client_ip, form_data.username, str(e))
        raise HTTPException(status_code=500, detail="خطا در ورود")

@app.post("/admin/login")
async def admin_login(request: Request, admin_data: dict):
    """Admin authentication"""
    client_ip = get_client_ip(request)
    
    try:
        logger.info(f"Admin login attempt from IP: {client_ip}")
        
        provided_code = admin_data.get("code", "")
        
        if not provided_code:
            log_security_event("admin_login_failed", client_ip, details="No admin code provided")
            raise HTTPException(status_code=400, detail="کد ادمین الزامی است")
        
        if provided_code != settings.admin_secret_code:
            log_security_event("admin_login_failed", client_ip, details=f"Invalid code: {provided_code}")
            raise HTTPException(status_code=401, detail="کد ادمین نامعتبر است")
        
        # Create admin token
        admin_token = create_access_token({
            "sub": "admin", 
            "role": "admin",
            "is_admin": True
        })
        
        log_security_event("admin_login_success", client_ip, "admin")
        logger.info(f"Successful admin login from IP: {client_ip}")
        
        return {
            "access_token": admin_token, 
            "token_type": "bearer", 
            "role": "admin",
            "message": "ورود ادمین موفقیت‌آمیز بود"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Admin login error: {str(e)}")
        log_security_event("admin_login_error", client_ip, details=str(e))
        raise HTTPException(status_code=500, detail="خطا در ورود ادمین")

# Protected endpoints
@app.get("/salons")
async def read_salons(
    current_user: BeautySalon = Depends(get_current_user),
    session: Session = Depends(get_db)
):
    """Get all salons (authenticated users only)"""
    salons = session.query(BeautySalon).all()
    return [
        {
            "id": salon.id,
            "username": salon.username,
            "name": salon.name,
            "address": salon.address,
            "phone": salon.phone,
            "instagram": salon.instagram,
            "description": salon.description
        }
        for salon in salons
    ]

@app.get("/verify-token")
async def verify_token(current_user: BeautySalon = Depends(get_current_user)):
    """Verify user token"""
    return {
        "username": current_user.username,
        "role": "user",
        "is_admin": False,
        "valid": True
    }

# Admin endpoints
@app.get("/admin/users")
async def get_all_users(
    session: Session = Depends(get_db),
    admin: dict = Depends(get_admin_user)
):
    """Get all users (admin only)"""
    users = session.query(BeautySalon).all()
    return [
        {
            "id": user.id,
            "username": user.username,
            "name": user.name,
            "address": user.address,
            "phone": user.phone,
            "instagram": user.instagram,
            "description": user.description
        }
        for user in users
    ]

# Error handlers
@app.exception_handler(404)
async def not_found_handler(request: Request, exc: HTTPException):
    """Custom 404 handler"""
    return HTMLResponse(
        content="""
        <!DOCTYPE html>
        <html lang="fa" dir="rtl">
        <head>
            <meta charset="UTF-8">
            <title>صفحه یافت نشد - Rosa</title>
            <style>
                body { font-family: 'Segoe UI', Tahoma, sans-serif; 
                       background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                       margin: 0; padding: 50px; text-align: center; color: white; }
                .container { max-width: 600px; margin: 0 auto; }
                h1 { font-size: 3rem; margin-bottom: 20px; }
                a { color: white; text-decoration: none; 
                    background: rgba(255,255,255,0.2); padding: 10px 20px; 
                    border-radius: 15px; }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>🌹 404</h1>
                <h2>صفحه یافت نشد</h2>
                <p>صفحه مورد نظر شما وجود ندارد.</p>
                <a href="/">🏠 بازگشت به خانه</a>
            </div>
        </body>
        </html>
        """,
        status_code=404
    )

# Include routers
try:
    from .routers import bookings, auth, services, reports
    app.include_router(bookings.router)
    app.include_router(auth.router)
    app.include_router(services.router)
    app.include_router(reports.router)
    logger.info("✅ All routers loaded successfully")
except ImportError as e:
    logger.error(f"❌ Could not import routers: {e}")
    print(f"Warning: Could not import routers: {e}")

# Startup and shutdown events
@app.on_event("startup")
async def startup_event():
    """Application startup tasks"""
    logger.info("🌹 Rosa Beauty Platform Starting...")
    
    try:
        # Create database tables
        create_tables()
        logger.info("✅ Database tables created/verified")
        
        # Initialize AI services
        if settings.openai_api_key:
            logger.info("✅ AI services initialized")
        else:
            logger.warning("⚠️ OpenAI API key not found - AI features disabled")
        
        logger.info("🚀 Rosa Beauty Platform started successfully!")
        
    except Exception as e:
        logger.error(f"❌ Startup failed: {e}")
        raise

@app.on_event("shutdown")
async def shutdown_event():
    """Application shutdown tasks"""
    logger.info("🌹 Rosa Beauty Platform shutting down...")
    logger.info("👋 Goodbye!")

# Development only
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level=settings.log_level.lower()
    )
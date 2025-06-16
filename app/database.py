from sqlalchemy import create_engine, event
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.engine import Engine
from .config import settings
import logging
import sqlite3

logger = logging.getLogger(__name__)

# تنظیمات مختلف برای انواع دیتابیس
def get_engine_config():
    """پیکربندی موتور دیتابیس بر اساس نوع"""
    config = {}
    
    if settings.database_type == "sqlite":
        config.update({
            "connect_args": {"check_same_thread": False},
            "echo": settings.debug
        })
        
        # فعال‌سازی Foreign Keys برای SQLite
        @event.listens_for(Engine, "connect")
        def set_sqlite_pragma(dbapi_connection, connection_record):
            if isinstance(dbapi_connection, sqlite3.Connection):
                cursor = dbapi_connection.cursor()
                cursor.execute("PRAGMA foreign_keys=ON")
                cursor.close()
    
    elif settings.database_type in ["mysql", "postgresql"]:
        config.update({
            "pool_pre_ping": True,
            "pool_recycle": 300,
            "echo": settings.debug
        })
    
    return config

# ایجاد موتور دیتابیس
try:
    engine_config = get_engine_config()
    engine = create_engine(settings.database_url, **engine_config)
    logger.info(f"Database engine created: {settings.database_type}")
except Exception as e:
    logger.error(f"Failed to create database engine: {e}")
    raise

# Session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for models
Base = declarative_base()

def get_db():
    """Dependency برای دریافت session دیتابیس"""
    db = SessionLocal()
    try:
        yield db
    except Exception as e:
        logger.error(f"Database error: {e}")
        db.rollback()
        raise
    finally:
        db.close()

def create_tables():
    """ایجاد جداول دیتابیس"""
    try:
        Base.metadata.create_all(bind=engine)
        logger.info("Database tables created successfully")
    except Exception as e:
        logger.error(f"Error creating tables: {e}")
        raise

def test_connection():
    """تست اتصال دیتابیس"""
    try:
        with engine.connect() as conn:
            if settings.database_type == "sqlite":
                result = conn.execute("SELECT 1").scalar()
            else:
                result = conn.execute("SELECT 1").scalar()
        
        logger.info(f"Database connection successful: {settings.database_type}")
        return True
    except Exception as e:
        logger.error(f"Database connection failed: {e}")
        return False
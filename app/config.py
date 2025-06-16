from pydantic_settings import BaseSettings
from typing import List, Optional
import os

class Settings(BaseSettings):
    # Database - انعطاف‌پذیر برای SQLite و MySQL/PostgreSQL
    database_type: str = "sqlite"  # sqlite, mysql, postgresql
    
    # SQLite (آفلاین - محلی)
    sqlite_database_path: str = "./rosa.db"
    
    # MySQL (برای cPanel)
    mysql_host: Optional[str] = None
    mysql_port: int = 3306
    mysql_user: Optional[str] = None
    mysql_password: Optional[str] = None
    mysql_database: Optional[str] = None
    
    # PostgreSQL (اختیاری)
    postgres_host: Optional[str] = None
    postgres_port: int = 5432
    postgres_user: Optional[str] = None
    postgres_password: Optional[str] = None
    postgres_database: Optional[str] = None
    
    # JWT
    secret_key: str = "rosa-secret-key-change-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    
    # AI (اختیاری)
    openai_api_key: Optional[str] = None
    openai_model: str = "gpt-3.5-turbo"
    
    # Environment
    environment: str = "development"  # development, production
    debug: bool = True
    log_level: str = "INFO"
    
    # CORS
    cors_origins: List[str] = ["*"]
    
    # Admin
    admin_secret_code: str = "Rosa2024Admin!@#"
    
    # Languages
    default_language: str = "fa"
    supported_languages: List[str] = ["fa", "ar", "en"]
    
    @property
    def database_url(self) -> str:
        """تولید URL دیتابیس بر اساس نوع"""
        if self.database_type == "sqlite":
            from pathlib import Path
            db_path = Path(self.sqlite_database_path).resolve()
            return f"sqlite:///{db_path}"
        
        elif self.database_type == "mysql":
            if not all([self.mysql_host, self.mysql_user, self.mysql_password, self.mysql_database]):
                raise ValueError("MySQL credentials are incomplete")
            return f"mysql+pymysql://{self.mysql_user}:{self.mysql_password}@{self.mysql_host}:{self.mysql_port}/{self.mysql_database}"
        
        elif self.database_type == "postgresql":
            if not all([self.postgres_host, self.postgres_user, self.postgres_password, self.postgres_database]):
                raise ValueError("PostgreSQL credentials are incomplete")
            return f"postgresql://{self.postgres_user}:{self.postgres_password}@{self.postgres_host}:{self.postgres_port}/{self.postgres_database}"
        
        else:
            raise ValueError(f"Unsupported database type: {self.database_type}")
    
    class Config:
        env_file = ".env"
        case_sensitive = False

settings = Settings()
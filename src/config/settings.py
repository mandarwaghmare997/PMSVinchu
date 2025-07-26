"""
Configuration Settings for PMS Intelligence Hub
Centralized configuration management using Pydantic
"""

import os
from typing import List, Optional, Dict, Any
from pydantic import BaseSettings, validator
from pathlib import Path

class Settings(BaseSettings):
    """Application settings with environment variable support"""
    
    # Application Settings
    APP_NAME: str = "PMS Intelligence Hub"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False
    
    # Database Settings
    DATABASE_URL: str = "postgresql://user:password@localhost:5432/pms_db"
    DATABASE_POOL_SIZE: int = 10
    DATABASE_MAX_OVERFLOW: int = 20
    
    # Salesforce Configuration
    SALESFORCE_USERNAME: Optional[str] = None
    SALESFORCE_PASSWORD: Optional[str] = None
    SALESFORCE_SECURITY_TOKEN: Optional[str] = None
    SALESFORCE_DOMAIN: str = "login"
    SALESFORCE_CLIENT_ID: Optional[str] = None
    SALESFORCE_CLIENT_SECRET: Optional[str] = None
    SALESFORCE_API_VERSION: str = "58.0"
    
    # Wealth Spectrum Configuration
    WEALTH_SPECTRUM_API_KEY: Optional[str] = None
    WEALTH_SPECTRUM_BASE_URL: Optional[str] = None
    WEALTH_SPECTRUM_USERNAME: Optional[str] = None
    WEALTH_SPECTRUM_PASSWORD: Optional[str] = None
    WEALTH_SPECTRUM_API_VERSION: str = "v1"
    
    # Security Settings
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    ALGORITHM: str = "HS256"
    
    # CORS Settings
    ALLOWED_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:8501"]
    ALLOWED_HOSTS: List[str] = ["localhost", "127.0.0.1"]
    
    # Cache Settings
    CACHE_TTL_SECONDS: int = 3600  # 1 hour
    REDIS_URL: Optional[str] = None
    
    # File Upload Settings
    MAX_FILE_SIZE_MB: int = 100
    ALLOWED_FILE_EXTENSIONS: List[str] = [".csv", ".xlsx", ".xls", ".pdf"]
    UPLOAD_DIR: str = "uploads"
    
    # Dashboard Settings
    DEFAULT_PAGE_SIZE: int = 50
    MAX_PAGE_SIZE: int = 1000
    DASHBOARD_REFRESH_INTERVAL: int = 300  # 5 minutes
    
    # Export Settings
    PDF_TEMPLATE_DIR: str = "templates/pdf"
    EXPORT_DIR: str = "exports"
    
    # Logging Settings
    LOG_LEVEL: str = "INFO"
    LOG_FILE: str = "logs/pms_hub.log"
    LOG_MAX_SIZE_MB: int = 10
    LOG_BACKUP_COUNT: int = 5
    
    # Email Settings (for reports)
    SMTP_HOST: Optional[str] = None
    SMTP_PORT: int = 587
    SMTP_USERNAME: Optional[str] = None
    SMTP_PASSWORD: Optional[str] = None
    SMTP_USE_TLS: bool = True
    
    # Performance Settings
    ENABLE_PROFILING: bool = False
    SLOW_QUERY_THRESHOLD: float = 1.0  # seconds
    
    # Feature Flags
    ENABLE_API_DOCS: bool = True
    ENABLE_METRICS_ENDPOINT: bool = True
    ENABLE_HEALTH_CHECK: bool = True
    ENABLE_AUDIT_LOGGING: bool = True
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True
    
    @validator("DATABASE_URL")
    def validate_database_url(cls, v):
        if not v or v == "postgresql://user:password@localhost:5432/pms_db":
            # Use SQLite for development if PostgreSQL not configured
            return "sqlite:///./pms_hub.db"
        return v
    
    @validator("ALLOWED_ORIGINS", pre=True)
    def parse_cors_origins(cls, v):
        if isinstance(v, str):
            return [origin.strip() for origin in v.split(",")]
        return v
    
    @validator("ALLOWED_HOSTS", pre=True)
    def parse_allowed_hosts(cls, v):
        if isinstance(v, str):
            return [host.strip() for host in v.split(",")]
        return v
    
    @validator("ALLOWED_FILE_EXTENSIONS", pre=True)
    def parse_file_extensions(cls, v):
        if isinstance(v, str):
            return [ext.strip() for ext in v.split(",")]
        return v
    
    def create_directories(self):
        """Create necessary directories"""
        directories = [
            self.UPLOAD_DIR,
            self.EXPORT_DIR,
            self.PDF_TEMPLATE_DIR,
            Path(self.LOG_FILE).parent,
            "cache"
        ]
        
        for directory in directories:
            Path(directory).mkdir(parents=True, exist_ok=True)
    
    def get_database_config(self) -> Dict[str, Any]:
        """Get database configuration dictionary"""
        return {
            "url": self.DATABASE_URL,
            "pool_size": self.DATABASE_POOL_SIZE,
            "max_overflow": self.DATABASE_MAX_OVERFLOW,
            "echo": self.DEBUG
        }
    
    def get_salesforce_config(self) -> Dict[str, Any]:
        """Get Salesforce configuration dictionary"""
        return {
            "username": self.SALESFORCE_USERNAME,
            "password": self.SALESFORCE_PASSWORD,
            "security_token": self.SALESFORCE_SECURITY_TOKEN,
            "domain": self.SALESFORCE_DOMAIN,
            "client_id": self.SALESFORCE_CLIENT_ID,
            "client_secret": self.SALESFORCE_CLIENT_SECRET,
            "api_version": self.SALESFORCE_API_VERSION
        }
    
    def get_wealth_spectrum_config(self) -> Dict[str, Any]:
        """Get Wealth Spectrum configuration dictionary"""
        return {
            "api_key": self.WEALTH_SPECTRUM_API_KEY,
            "base_url": self.WEALTH_SPECTRUM_BASE_URL,
            "username": self.WEALTH_SPECTRUM_USERNAME,
            "password": self.WEALTH_SPECTRUM_PASSWORD,
            "api_version": self.WEALTH_SPECTRUM_API_VERSION
        }
    
    def is_production(self) -> bool:
        """Check if running in production environment"""
        return not self.DEBUG and os.getenv("ENVIRONMENT", "development") == "production"
    
    def get_cors_config(self) -> Dict[str, Any]:
        """Get CORS configuration"""
        return {
            "allow_origins": self.ALLOWED_ORIGINS,
            "allow_credentials": True,
            "allow_methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
            "allow_headers": ["*"]
        }

# Global settings instance
_settings = None

def get_settings() -> Settings:
    """Get global settings instance (singleton pattern)"""
    global _settings
    if _settings is None:
        _settings = Settings()
        _settings.create_directories()
    return _settings

# Environment-specific configurations
class DevelopmentSettings(Settings):
    """Development environment settings"""
    DEBUG: bool = True
    LOG_LEVEL: str = "DEBUG"
    ENABLE_API_DOCS: bool = True
    ENABLE_PROFILING: bool = True

class ProductionSettings(Settings):
    """Production environment settings"""
    DEBUG: bool = False
    LOG_LEVEL: str = "WARNING"
    ENABLE_API_DOCS: bool = False
    ENABLE_PROFILING: bool = False
    
    @validator("SECRET_KEY")
    def validate_secret_key(cls, v):
        if v == "your-secret-key-change-in-production":
            raise ValueError("Secret key must be changed in production")
        return v

class TestingSettings(Settings):
    """Testing environment settings"""
    DEBUG: bool = True
    DATABASE_URL: str = "sqlite:///./test_pms_hub.db"
    LOG_LEVEL: str = "DEBUG"
    CACHE_TTL_SECONDS: int = 1  # Short cache for testing

def get_settings_for_environment(environment: str = None) -> Settings:
    """Get settings for specific environment"""
    if environment is None:
        environment = os.getenv("ENVIRONMENT", "development")
    
    settings_map = {
        "development": DevelopmentSettings,
        "production": ProductionSettings,
        "testing": TestingSettings
    }
    
    settings_class = settings_map.get(environment, Settings)
    settings = settings_class()
    settings.create_directories()
    return settings

# Configuration validation
def validate_configuration(settings: Settings) -> List[str]:
    """Validate configuration and return list of warnings/errors"""
    warnings = []
    
    # Check database configuration
    if "sqlite" in settings.DATABASE_URL and settings.is_production():
        warnings.append("Using SQLite in production is not recommended")
    
    # Check Salesforce configuration
    sf_config = settings.get_salesforce_config()
    if not all([sf_config["username"], sf_config["password"], sf_config["security_token"]]):
        warnings.append("Salesforce configuration is incomplete - API integration will not work")
    
    # Check Wealth Spectrum configuration
    ws_config = settings.get_wealth_spectrum_config()
    if not all([ws_config["api_key"], ws_config["base_url"]]):
        warnings.append("Wealth Spectrum configuration is incomplete - API integration will not work")
    
    # Check security settings
    if settings.SECRET_KEY == "your-secret-key-change-in-production" and settings.is_production():
        warnings.append("SECRET_KEY must be changed in production")
    
    # Check file upload settings
    if settings.MAX_FILE_SIZE_MB > 500:
        warnings.append("MAX_FILE_SIZE_MB is very large - consider reducing for security")
    
    return warnings

# Configuration loader for different deployment scenarios
class ConfigLoader:
    """Configuration loader with support for different sources"""
    
    @staticmethod
    def from_env_file(file_path: str) -> Settings:
        """Load configuration from environment file"""
        settings = Settings(_env_file=file_path)
        settings.create_directories()
        return settings
    
    @staticmethod
    def from_dict(config_dict: Dict[str, Any]) -> Settings:
        """Load configuration from dictionary"""
        settings = Settings(**config_dict)
        settings.create_directories()
        return settings
    
    @staticmethod
    def from_json_file(file_path: str) -> Settings:
        """Load configuration from JSON file"""
        import json
        with open(file_path, 'r') as f:
            config_dict = json.load(f)
        return ConfigLoader.from_dict(config_dict)
    
    @staticmethod
    def from_yaml_file(file_path: str) -> Settings:
        """Load configuration from YAML file"""
        try:
            import yaml
            with open(file_path, 'r') as f:
                config_dict = yaml.safe_load(f)
            return ConfigLoader.from_dict(config_dict)
        except ImportError:
            raise ImportError("PyYAML is required to load YAML configuration files")

# Export commonly used functions and classes
__all__ = [
    "Settings",
    "get_settings",
    "get_settings_for_environment",
    "validate_configuration",
    "ConfigLoader",
    "DevelopmentSettings",
    "ProductionSettings",
    "TestingSettings"
]


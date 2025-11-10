"""Configuration management using pydantic settings."""
from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # Gemini API Configuration
    gemini_key: str = ""
    
    # SendGrid Configuration
    sendgrid_api_key: str = ""
    sendgrid_from_email: str = "noreply@stakesync.com"
    
    # Database Configuration
    database_url: str = "sqlite:///./stake_sync.db"
    
    # Server Configuration
    host: str = "0.0.0.0"
    port: int = 8000
    
    # Optional: JWT Secret for Auth
    secret_key: str = "change_this_secret_key_in_production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    
    class Config:
        env_file = ".env"
        case_sensitive = False


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()

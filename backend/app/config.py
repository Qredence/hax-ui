from pydantic_settings import BaseSettings
from pydantic import ConfigDict
from typing import List
import os


class Settings(BaseSettings):
    model_config = ConfigDict(
        env_file=".env",
        case_sensitive=False,
        extra="ignore"
    )
    
    # API Configuration
    api_v1_str: str = "/api/v1"
    project_name: str = "HAX UI API"
    version: str = "1.0.0"
    description: str = "Backend API for HAX UI Chat System"
    
    # Security
    secret_key: str = "dev-secret-key-change-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    
    # Database
    database_url: str = "sqlite:///./test.db"
    
    # Redis (for caching and sessions)
    redis_url: str = "redis://localhost:6379/0"
    
    # CORS
    allowed_origins: str = "http://localhost:8080,http://127.0.0.1:8080"
    
    def get_allowed_origins_list(self) -> List[str]:
        """Convert comma-separated origins string to list."""
        if isinstance(self.allowed_origins, str):
            return [origin.strip() for origin in self.allowed_origins.split(",")]
        return self.allowed_origins
    
    # Gemini AI
    gemini_api_key: str = "test-api-key"
    gemini_model_id: str = "gemini-2.5-flash"
    
    # Environment
    debug: bool = False


def get_settings() -> Settings:
    """Get settings instance, allowing for test overrides"""
    # Check if we're in test mode
    if os.getenv("PYTEST_CURRENT_TEST"):
        return Settings(
            database_url="sqlite:///:memory:",
            secret_key="test-secret-key",
            gemini_api_key="test-gemini-key",
            debug=True
        )
    return Settings()


settings = get_settings()
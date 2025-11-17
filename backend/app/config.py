from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional


class Settings(BaseSettings):
    """Application settings loaded from environment variables"""
    
    # FastAPI
    app_host: str = "127.0.0.1"
    app_port: int = 8000
    secret_key: str
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 60
    
    # MongoDB
    mongodb_uri: str
    mongodb_db: str = "credsaathi_db"
    
    # Google OAuth
    google_client_id: str
    google_client_secret: str
    google_oauth_redirect_uri: str
    
    # CORS
    frontend_url: str = "http://localhost:8080"
    
    # Optional
    sentry_dsn: Optional[str] = None

    # Gemini API
    gemini_api_key: str
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False
    )


settings = Settings()

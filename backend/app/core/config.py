import os
from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    PROJECT_NAME: str = "SmartStock AI"
    API_V1_STR: str = ""
    
    # MongoDB
    MONGODB_URI: str = os.getenv("MONGODB_URI", "mongodb://localhost:27017")
    MONGODB_DB_NAME: str = os.getenv("MONGODB_DB_NAME", "smartstock")
    
    # Security
    JWT_SECRET_KEY: str = os.getenv("JWT_SECRET_KEY", "change_this_secret_key_in_production")
    JWT_ALGORITHM: str = os.getenv("JWT_ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # CORS
    BACKEND_CORS_ORIGINS: list[str] = [
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ]

    class Config:
        case_sensitive = True

@lru_cache()
def get_settings():
    return Settings()

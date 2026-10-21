import os
from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    PROJECT_NAME: str = "SkillVerse AI"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api"
    
    # Database
    DATABASE_URL: str = os.getenv("DATABASE_URL", "postgresql+psycopg2://postgres:postgrespassword@localhost:5432/skillverse")
    
    # JWT Authentication
    SECRET_KEY: str = os.getenv("SECRET_KEY", "skillverse_super_secret_jwt_key_9827349827348923748923")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440  # 24 hours
    
    # Optional AI
    OPENAI_API_KEY: Optional[str] = os.getenv("OPENAI_API_KEY", None)

    class Config:
        env_file = ".env"
        extra = "allow"

settings = Settings()

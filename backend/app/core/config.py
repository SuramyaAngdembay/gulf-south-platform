from typing import List, Union, Optional
from pydantic import AnyHttpUrl, validator
from pydantic_settings import BaseSettings
import os
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    PROJECT_NAME: str = "Gulf South Platform"
    API_V1_STR: str = "/api/v1"
    
    # Server settings
    PORT: int = 5000
    NODE_ENV: str = "development"
    
    # CORS
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []

    @validator("BACKEND_CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    # Database
    DB_HOST: str = "localhost"
    DB_USER: str = "root"
    DB_PASSWORD: Optional[str] = None
    DB_NAME: str = "gulf_south_platform"
    DATABASE_URL: Optional[str] = None
    SQLALCHEMY_DATABASE_URI: Optional[str] = None

    @validator("SQLALCHEMY_DATABASE_URI", pre=True)
    def assemble_db_uri(cls, v: Optional[str], values: dict) -> str:
        if v:
            return v
        if values.get("DATABASE_URL"):
            return values["DATABASE_URL"]
        # Default to SQLite if no DATABASE_URL is provided
        return os.getenv(
            "DATABASE_URL",
            f"sqlite:///./app.db"
        )

    # JWT
    JWT_SECRET: str = "your-secret-key-here"
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your-secret-key-here")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8  # 8 days

    class Config:
        case_sensitive = True
        env_file = ".env"

settings = Settings() 
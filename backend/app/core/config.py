from pydantic_settings import BaseSettings
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]

class Settings(BaseSettings):
    DATABASE_URL: str

    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    REFRESH_TOKEN_EXPIRE_MINUTES: int

    class Config:
        env_file = os.getenv("ENV_FILE", BASE_DIR / ".env.dev"),
        extra = "allow"

settings = Settings()

from pydantic_settings import BaseSettings
import os

class Settings(BaseSettings):
    DATABASE_URL: str

    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    REFRESH_TOKEN_EXPIRE_MINUTES: int

    class Config:
        env_file = os.getenv("ENV_FILE", ".env")
        extra = "allow"

settings = Settings()

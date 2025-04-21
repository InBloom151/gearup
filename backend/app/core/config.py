from __future__ import annotations

import os
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parents[2]


class Settings(BaseSettings):
    # --- Database ---
    DATABASE_URL: str

    # --- Security / JWT ---
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    REFRESH_TOKEN_EXPIRE_MINUTES: int

    # --- App behaviour ---
    APP_ENV: str
    LOG_LEVEL: str

    model_config = SettingsConfigDict(
        env_file=os.getenv(
            "ENV_FILE", BASE_DIR / f".env.{os.getenv('APP_ENV', 'dev')}"
        ),
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="allow",
    )


settings = Settings()

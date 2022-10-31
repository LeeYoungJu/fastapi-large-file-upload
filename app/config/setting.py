import secrets

from typing import List, Optional
from pydantic import BaseSettings, AnyHttpUrl


class Settings(BaseSettings):
    API_V1: str = "/api/v1"
    # API_V2: str = "/api/v2"

    SECRET_KEY: str = secrets.token_urlsafe(32)

    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []

    PROJECT_NAME: str

    DB_TYPE: str

    MARIA_DB_SERVER: str
    MARIA_DB_USER: str
    MARIA_DB_PASSWORD: str
    MARIA_DB: str

    class Config:
        env_file = ".env"


settings = Settings()

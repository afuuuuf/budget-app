from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):
    DATABASE_URL: str
    HOST: str = "127.0.0.1"
    PORT: int = 8000
    RELOAD: bool = True
    CORS_ORIGINS: List[str] = ["http://localhost:3000"]

    class Config:
        env_file = ".env"

settings = Settings()
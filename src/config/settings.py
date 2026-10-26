from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str
    HOST: str = "127.0.0.1"
    PORT: int = 8000
    RELOAD: bool = True
    CORS_ORIGINS: list[str] = ["http://localhost:3000"]
    JWT_SECRET: str = "dev-only-secret-change-before-deploy"
    JWT_ALGORITHM: str = "HS256"

    class Config:
        env_file = ".env"


settings = Settings()

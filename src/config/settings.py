from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str
    HOST: str = "127.0.0.1"
    PORT: int = 8000
    RELOAD: bool = True

    class Config:
        env_file = ".env"


settings = Settings()

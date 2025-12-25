from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql+asyncpg://easy_writer:password@easy_writer_postgres:5432/easy_writer_db"
    REDIS_URL: str = "redis://easy_writer_redis:6379/0"
    CELERY_BROKER_URL: str = "redis://easy_writer_redis:6379/4"
    CELERY_RESULT_BACKEND: str = "redis://easy_writer_redis:6379/5"
    SECRET_KEY: str = "change-me-in-production"
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRE_MINUTES: int = 1440
    DEBUG: bool = False
    ENVIRONMENT: str = "development"
    CORS_ORIGINS: str = "http://localhost:3000"

    class Config:
        env_file = ".env"

settings = Settings()


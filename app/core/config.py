from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Application Settings
    APP_NAME: str = "Finance System API"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True

    # Database Settings
    DATABASE_URL: str = "sqlite:///./finance_system.db"

    # JWT Settings
    SECRET_KEY: str = "your-super-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # Financial Health Score Thresholds
    HEALTHY_SAVINGS_RATE: float = 0.20
    WARNING_EXPENSE_RATE: float = 0.80

    class Config:
        env_file = ".env"


settings = Settings()
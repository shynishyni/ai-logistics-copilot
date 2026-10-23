import os
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    PROJECT_NAME: str = "AI Logistics Copilot"
    API_V1_STR: str = "/api/v1"
    GEMINI_API_KEY: str = ""
    DATABASE_URL: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/logistics_db"
    REDIS_URL: str = "redis://localhost:6379/0"
    MCP_SERVER_URL: str = "http://localhost:8001"
    LOG_LEVEL: str = "INFO"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

settings = Settings()

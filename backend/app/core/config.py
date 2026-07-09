from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    app_name: str = "AI-First CRM for HCP"
    api_prefix: str = "/api/v1"
    environment: str = "development"
    database_url: str = "sqlite:///./hcp_crm.db"
    create_tables_on_start: bool = True
    secret_key: str = Field("change-me-before-production", min_length=16)
    access_token_minutes: int = 60
    cors_origins: list[str] = ["http://localhost:5173"]
    groq_api_key: str | None = None
    groq_model: str = "gemma2-9b-it"


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()

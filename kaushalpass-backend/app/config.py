"""Application settings — all env vars loaded here."""

from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    APP_NAME: str = "KaushalPass API"
    APP_VERSION: str = "1.0"
    DEBUG: bool = False

    # CORS
    CORS_ORIGINS: list[str] = Field(
        default=["http://localhost:3000", "https://kaushalpass.in"]
    )

    # Supabase
    SUPABASE_URL: str
    SUPABASE_SERVICE_ROLE_KEY: str
    SUPABASE_JWT_SECRET: str = ""
    SUPABASE_JWKS_URL: str = ""

    # Redis (Upstash)
    REDIS_URL: str = "redis://localhost:6379"

    # Sarvam AI
    SARVAM_API_KEY: str

    # NVIDIA NIM — GLM 5.1
    NVIDIA_API_KEY: str
    NVIDIA_API_BASE: str = "https://integrate.api.nvidia.com/v1"
    GLM_MODEL: str = "z-ai/glm-5.1"

    # Rate limits
    VOICE_ASSESS_DAILY_LIMIT: int = 10
    RATE_LIMIT_WINDOW_SECONDS: int = 86400

    # Storage
    TTS_BUCKET: str = "tts-audio"
    TTS_SIGNED_URL_EXPIRY_SECONDS: int = 3600

    # JWKS cache TTL
    JWKS_CACHE_TTL_SECONDS: int = 3600


@lru_cache
def get_settings() -> Settings:
    return Settings()

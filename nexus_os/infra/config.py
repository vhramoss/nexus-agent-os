from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="NEXUS_",
        env_file=".env",
        case_sensitive=False,
        extra="ignore",
    )

    # --------------------
    # Runtime
    # --------------------
    max_concurrent: int = Field(default=3, ge=1, le=100)
    exec_timeout: int = Field(default=10, ge=1)
    agent_max_loops: int = Field(default=5, ge=1)

    # --------------------
    # Storage
    # --------------------
    events_dir: str = "events"
    memory_path: str = "memory.json"

    # --------------------
    # Redis
    # --------------------
    use_redis: bool = False
    redis_url: str = "redis://localhost:6379"

    # --------------------
    # Feature flags
    # --------------------
    simulate_executor_failure: bool = False


@lru_cache
def get_settings() -> Settings:
    return Settings()

from functools import lru_cache
from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):

    env: str = Field(
        default="local",
        description="Ambiente de execução: local, staging ou prod",
    )

    log_level: str = Field(
        default="INFO",
        description="Nível global de log (DEBUG, INFO, WARNING, ERROR)",
    )

    database_url: str = Field(
        ...,
        description="URL de conexão com o banco de dados principal",
    )

    redis_url: str = Field(
        ...,
        description="URL de conexão com o Redis",
    )

    agent_max_loops: int = Field(
        default=25,
        description="Número máximo de ciclos de execução de um agente",
    )

    agent_timeout_seconds: int = Field(
        default=300,
        description="Timeout máximo para execução de um agente (em segundos)",
    )

    class Config:
        env_file = ".env"
        case_sensitive = False


@lru_cache
def get_settings() -> Settings:

    return Settings()
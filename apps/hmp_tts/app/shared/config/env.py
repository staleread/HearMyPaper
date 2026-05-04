from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class EnvSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env.development", env_file_encoding="utf-8")

    rabbitmq_url: str = "amqp://guest:guest@rabbitmq:5672/"
    minio_url: str = "http://minio:9000"
    minio_access_key: str = "minioadmin"
    minio_secret_key: str = "minioadmin"
    
    # SPIRE/SPIFFE configuration
    spiffe_endpoint_socket: str = "unix:///run/spire/sockets/agent.sock"


@lru_cache
def get_env_settings() -> "EnvSettings":
    return EnvSettings()

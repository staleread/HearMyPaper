from functools import lru_cache
from pydantic import computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict


class EnvSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env.development", env_file_encoding="utf-8")

    jwt_secret: str = "4jez3Ruh5sbVMChP"
    jwt_algorithm: str = "HS256"
    jwt_lifetime_sec: int = 90000

    postgres_user: str = "user"
    postgres_password: str = "password"
    postgres_host: str = "postgres"
    postgres_port: str = "5432"
    postgres_db: str = "hmp-postgres"

    redis_host: str = "redis"
    redis_port: int = 6379
    redis_db: int = 0
    redis_password: str = "password"
    redis_user: str = "default"

    rabbitmq_url: str = "amqp://guest:guest@rabbitmq:5672/"

    minio_url: str = "http://minio:9000"
    minio_access_key: str = "minioadmin"
    minio_secret_key: str = "minioadmin"

    @computed_field
    @property
    def postgres_url(self) -> str:
        return f"postgresql+psycopg2://{self.postgres_user}:{self.postgres_password}@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"

    @computed_field
    @property
    def redis_url(self) -> str:
        return f"redis://{self.redis_user}:{self.redis_password}@{self.redis_host}:{self.redis_port}/{self.redis_db}"


@lru_cache
def get_env_settings() -> "EnvSettings":
    return EnvSettings()

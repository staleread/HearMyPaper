from functools import lru_cache

from pydantic import Field, computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict


class PostgresSettings(BaseSettings):
    user: str = "user"
    password: str = "password"
    host: str = "postgres"
    port: int = 5432
    db: str = "hmp-postgres"

    @computed_field
    @property
    def url(self) -> str:
        return f"postgresql+asyncpg://{self.user}:{self.password}@{self.host}:{self.port}/{self.db}"


class RedisSettings(BaseSettings):
    host: str = "redis"
    port: int = 6379
    db: int = 0
    password: str = "password"
    user: str = "default"

    @computed_field
    @property
    def url(self) -> str:
        return f"redis://{self.user}:{self.password}@{self.host}:{self.port}/{self.db}"


class RabbitMQSettings(BaseSettings):
    url: str = "amqp://guest:guest@rabbitmq:5672/"


class JWTSettings(BaseSettings):
    secret: str = "secret"
    algorithm: str = "HS256"
    lifetime_sec: int = 90000
    audience: str = "hearmypaper"
    issuer: str = "hearmypaper-leader"


class MinioSettings(BaseSettings):
    url: str = "http://minio:9000"
    public_url: str | None = None
    access_key: str = "minioadmin"
    secret_key: str = "minioadmin"


class InitUserSettings(BaseSettings):
    id: str = "admin"
    name: str = "Admin"
    surname: str = "User"
    email: str = "admin@hmp.local"
    public_key_b64: str = ""


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=(".env.development", ".env.local"),
        env_file_encoding="utf-8",
        env_nested_delimiter="__",
        extra="ignore",
    )

    postgres: PostgresSettings = Field(default_factory=PostgresSettings)
    redis: RedisSettings = Field(default_factory=RedisSettings)
    minio: MinioSettings = Field(default_factory=MinioSettings)
    rabbitmq: RabbitMQSettings = Field(default_factory=RabbitMQSettings)
    jwt: JWTSettings = Field(default_factory=JWTSettings)
    init_user: InitUserSettings = Field(default_factory=InitUserSettings)


@lru_cache
def get_settings():
    return Settings()

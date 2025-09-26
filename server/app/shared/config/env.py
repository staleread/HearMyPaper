from pydantic import computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict


class PostrgresSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_prefix="postgres_")

    user: str
    password: str
    host: str
    port: str = "5432"
    database: str

    @computed_field  # type: ignore
    @property
    def url(self) -> str:
        return f"postgresql+psycopg2://{self.user}:{self.password}@{self.host}:{self.port}/{self.database}"


class JwtSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_prefix="jwt_")

    cookie_name: str
    secret: str
    algorithm: str
    lifetime: int


class EnvSettings(BaseSettings):
    postgres: PostrgresSettings
    jwt: JwtSettings


env_settings = EnvSettings()  # type: ignore

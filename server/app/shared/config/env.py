from pydantic import computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict


class EnvSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")

    jwt_secret: str
    jwt_algorithm: str
    jwt_lifetime_sec: int

    postgres_user: str
    postgres_password: str
    postgres_host: str
    postgres_port: str = "5432"
    postgres_db: str

    server_private_key_password: str

    @computed_field  # type: ignore
    @property
    def postgres_url(self) -> str:
        return f"postgresql+psycopg2://{self.postgres_user}:{self.postgres_password}@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"


env_settings = EnvSettings()  # type: ignore

from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field


class Settings(BaseSettings):
    back_port: int = Field(default=8007)
    postgres_user: str = Field(default="postgres")
    postgres_password: str = Field(default="<PASSWORD>")
    postgres_db: str = Field(default="postgres")
    postgres_host: str = Field(default="postgres")
    db_port: int = Field(default=5432)
    redis_url: str = Field(default="redis://localhost:6379/0")
    redis_timeout: int = Field(default=600)
    model_config = SettingsConfigDict(env_file="../.env.dev")


settings = Settings()

if __name__ == "__main__":
    print(settings.dict())

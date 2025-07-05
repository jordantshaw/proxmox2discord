from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import field_validator


class Settings(BaseSettings):
    log_directory: Path = Path().cwd() / "logs"
    # log_retention_days: int = 7

    @field_validator("log_directory", mode='after')
    def create_log_directory(cls, v):
        v.mkdir(parents=True, exist_ok=True)
        return v

    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8')


settings = Settings()
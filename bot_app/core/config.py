"""Настройки проекта."""
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file='.env', env_file_encoding='utf-8'
    )
    bot_token: str
    database_url: str = 'sqlite+aiosqlite:///./random_coffe_bot.db'


settings = Settings()

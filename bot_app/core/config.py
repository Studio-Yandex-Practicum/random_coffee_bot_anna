"""Настройки проекта."""
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file='.env', env_file_encoding='utf-8'
    )
    bot_token: str = "6067823117:AAHhcr-xgoqZoHGmj-aW9oyfK6WOZuDM4w8"
    database_url: str = "sqlite+aiosqlite:///./random_coffe_bot.db"
    gen_admin_id: int


settings = Settings()

# DB_URL=postgresql+asyncpg://login:password@localhost:5432/db_name

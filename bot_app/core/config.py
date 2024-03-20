"""Настройки проекта."""
from pydantic_settings import BaseSettings, SettingsConfigDict
from aiogram import Bot


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file='.env', env_file_encoding='utf-8'
    )
    bot_token: str = "6067823117:AAHhcr-xgoqZoHGmj-aW9oyfK6WOZuDM4w8"
    database_url: str
    gen_admin_id: int


settings = Settings()
bot = Bot(settings.bot_token)

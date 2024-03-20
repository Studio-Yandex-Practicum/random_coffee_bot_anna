"""Настройки проекта."""
from pydantic_settings import BaseSettings, SettingsConfigDict
from aiogram import Bot
from aiogram.enums import ParseMode
from aiogram.client.bot import DefaultBotProperties


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file='.env', env_file_encoding='utf-8'
    )
    bot_token: str
    database_url: str
    gen_admin_id: int


settings = Settings()
bot = Bot(settings.bot_token,
          default=DefaultBotProperties(parse_mode=ParseMode.HTML))

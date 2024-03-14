"""Настройки проекта."""
from pydantic_settings import BaseSettings, SettingsConfigDict
class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file='.env', env_file_encoding='utf-8'
    )
    bot_token: str
    bot_token: str = '6821461797:AAESNlZFrLC-gdHECpwwIao6A3Hs4-NmCo0'
    database_url: str = 'sqlite+aiosqlite:///./random_coffe_bot.db'


settings = Settings()

# DB_URL=postgresql+asyncpg://login:password@localhost:5432/db_name
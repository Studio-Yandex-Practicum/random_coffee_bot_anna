"""Настройки работы с базой данных"""
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from bot_app.core.config import settings

engine = create_async_engine(settings.database_url, echo=True)

async_session = async_sessionmaker(engine, expire_on_commit=False)


async def get_async_session():
    """Асинхронный генератор сессий."""
    async with async_session() as session:
        yield session

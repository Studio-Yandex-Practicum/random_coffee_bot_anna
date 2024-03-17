"""Настройки работы с базой данных"""
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from core.config import settings

engine = create_async_engine(settings.DATABASE_URL, echo=True)

session_maker = async_sessionmaker(engine, expire_on_commit=False)


async def get_async_session():
    """Асинхронный генератор сессий."""
    async with session_maker() as session:
        yield session

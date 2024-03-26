from aiogram import Bot, types
from aiogram.filters import Filter
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from bot_app.database.models import User
from bot_app.core.config import settings


class IsAdmin(Filter):
    """Filter for admin."""
    def __init__(self) -> None:
        pass

    async def __call__(self, message: types.Message, bot: Bot,
                       session: AsyncSession) -> bool:
        result = await session.execute(
            select(User).filter(User.tg_id == message.from_user.id)
        )
        user = result.scalars().one_or_none()
        if user.is_admin or message.from_user.id == settings.gen_admin_id:
            return True
        else:
            return False

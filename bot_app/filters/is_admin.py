from aiogram import Bot, types
from aiogram.filters import Filter


class IsAdmin(Filter):
    """Фильтр для админа."""
    def __init__(self) -> None:
        pass

    async def __call__(self, message: types.Message, bot: Bot) -> bool:
        return int(message.from_user.id) == 617537024  # поменять на свой тг id

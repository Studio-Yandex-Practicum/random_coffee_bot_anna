from aiogram import Bot, types
from aiogram.filters import Filter

admin_ids = [117732520] 

class IsAdmin(Filter):
    """Фильтр для админа."""
    def __init__(self) -> None:
        pass

    async def __call__(self, message: types.Message, bot: Bot) -> bool:
        return int(message.from_user.id) in admin_ids


async def add_admin_id(new_id: int):
    """Добавить новый id в список администраторов."""
    admin_ids.append(new_id)

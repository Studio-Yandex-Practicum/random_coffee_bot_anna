import asyncio

from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart
from aiogram.types import Message

from bot_app.core.config import settings

bot = Bot(settings.bot_token)
dp = Dispatcher()


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await message.answer("Hi")


async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)  # необходимо убрать при размещении на сервере


asyncio.run(main())

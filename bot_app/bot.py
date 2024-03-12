import pytz

import asyncio
from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart
from aiogram.types import Message
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from bot_app.core.config import settings

bot = Bot(settings.bot_token)
dp = Dispatcher()
timezone = pytz.timezone('Europe/Moscow')
scheduler = AsyncIOScheduler(timezone=timezone)


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await message.answer("Hi")


async def send_messages_mon():
    await bot.send_message(user_tg_id, 'Здесь будет рассылка по пн')


async def send_messages_fri():
    await bot.send_message(user_tg_id, 'Здесь будет рассылка по птн')


def schedule_jobs_mon():
    """Отправка рассылки по понедельникам."""
    scheduler.add_job(send_messages_mon, trigger="cron",
                      day_of_week='mon', hour=10, minute=30)


def schedule_jobs_fri():
    """Отправка рассылки по пятницам."""
    scheduler.add_job(send_messages_mon, trigger="cron",
                      day_of_week='fri', hour=10, minute=30)


async def main():
    schedule_jobs_mon()
    schedule_jobs_fri()
    scheduler.start()
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)  # необходимо убрать при размещении на сервере


asyncio.run(main())

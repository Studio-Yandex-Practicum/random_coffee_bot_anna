import asyncio
import pytz
from aiogram import Dispatcher, types
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from bot_app.core.config import bot
from bot_app.database.engine import session_maker, get_async_session
from bot_app.handlers.admin import admin_router
from bot_app.handlers.base_commands import base_commands_router
from bot_app.handlers.user_registration import user_reg_router
from bot_app.handlers.callbacks_handler import callback_router
from bot_app.middleware.dp import DataBaseSession
from bot_app.mailing.mailing import meeting_reminder_mailing


async def on_startup():
    print('Бот запущен')


async def on_shutdown():
    print('Бот лег')


async def main() -> None:
    dp = Dispatcher()
    dp.include_router(user_reg_router)
    dp.include_router(base_commands_router)
    dp.include_router(callback_router)
    dp.include_router(admin_router)
    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)
    dp.update.middleware(DataBaseSession(session_pool=session_maker))

    timezone = pytz.timezone('Europe/Moscow')
    scheduler = AsyncIOScheduler(timezone=timezone)

    sql_session = await anext(get_async_session())
    scheduler.add_job(meeting_reminder_mailing,
                      args=(sql_session,), trigger='cron',
                      day_of_week='fri', hour=10, minute=30)
    scheduler.start()

    await bot.delete_my_commands(scope=types.BotCommandScopeAllPrivateChats())
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())


asyncio.run(main())

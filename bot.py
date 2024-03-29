import asyncio
from datetime import datetime

from aiogram import Dispatcher, types
from aiogram.types import BotCommand
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from bot_app.core.config import TIMEZONE, bot
from bot_app.core.constants import Commands, MailingInt, MailingStr, Messages
from bot_app.database.engine import get_async_session, session_maker
from bot_app.mailing.mailing import (meeting_reminder_mailing,
                                     newsletter_about_the_meeting)
from bot_app.middleware.dp import DataBaseSession
from bot_app.routers import main_router


async def on_startup():
    """Startup message."""
    print(Messages.START_UP_MSG)


async def on_shutdown():
    """Shutdown message."""
    print(Messages.SHUT_DOWN_MSG)


COMMANDS = [
    BotCommand(command="/start", description=Commands.BOT_RESTART),
    BotCommand(command="/admin", description=Commands.ADMIN_PANEL),
    BotCommand(command="/help", description=Commands.HELP),
]


async def main() -> None:
    dp = Dispatcher()
    dp.include_router(main_router)
    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)
    dp.update.middleware(DataBaseSession(session_pool=session_maker))

    scheduler = AsyncIOScheduler(timezone=TIMEZONE)
    sql_session = await anext(get_async_session())

# ДЛЯ ТЕСТИРОВАНИЯ РАССЫЛКИ НА ПН НУЖНО РАЗКОММЕНТИРОВАТЬ СЛЕД 2 СТРОКИ, РАССЫЛКА БУДЕТ ПРОИСХОДИТЬ ПРИ ЗАПУСКЕ БОТА
    # scheduler.add_job(newsletter_about_the_meeting, args=(sql_session,),
    #                   next_run_time=datetime.now())
    # scheduler.add_job(
    #     newsletter_about_the_meeting, args=(sql_session,),
    #     trigger=MailingStr.TRIGGER,
    #     day_of_week=MailingStr.MAIL_TO_COUPLES_DAY,
    #     hour=MailingInt.MAIL_TO_COUPLES_HOUR,
    #     minute=MailingInt.MAIL_TO_COUPLES_MIN
    # )

    scheduler.add_job(newsletter_about_the_meeting, args=(sql_session,),
                      trigger=MailingStr.TRIGGER, day_of_week='0-6',
                      hour=10, minute=00)

    scheduler.add_job(newsletter_about_the_meeting, args=(sql_session,),
                      trigger=MailingStr.TRIGGER, day_of_week='0-6',
                      hour=14, minute=00)

# ДЛЯ ТЕСТИРОВАНИЯ РАССЫЛКИ НА ПТН НУЖНО РАЗКОММЕНТИРОВАТЬ СЛЕД 2 СТРОКИ, РАССЫЛКА БУДЕТ ПРОИСХОДИТЬ ПРИ ЗАПУСКЕ БОТА
    # scheduler.add_job(meeting_reminder_mailing, args=(
    #     sql_session,), next_run_time=datetime.now())
    # scheduler.add_job(
    #     meeting_reminder_mailing, args=(sql_session,),
    #     trigger=MailingStr.TRIGGER,
    #     day_of_week=MailingStr.REMIND_MAIL_DAY,
    #     hour=MailingInt.REMIND_MAIL_HOUR,
    #     minute=MailingInt.REMIND_MAIL_MIN)

    scheduler.add_job(meeting_reminder_mailing, args=(sql_session,),
                      trigger=MailingStr.TRIGGER,
                      day_of_week='0-6', hour=12, minute=00)

    scheduler.add_job(meeting_reminder_mailing, args=(sql_session,),
                      trigger=MailingStr.TRIGGER,
                      day_of_week='0-6', hour=16, minute=00)

    scheduler.start()

    await bot.delete_my_commands(scope=types.BotCommandScopeAllPrivateChats())
    await bot.delete_webhook(drop_pending_updates=True)
    try:
        await dp.start_polling(bot,
                               allowed_updates=dp.resolve_used_update_types())
    finally:
        await bot.session.close()

asyncio.run(main())

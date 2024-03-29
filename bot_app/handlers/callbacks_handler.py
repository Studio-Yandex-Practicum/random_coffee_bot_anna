import asyncio
from aiogram import F, Router, types
from bot_app.core.config import bot
from bot_app.core.constants import Messages
from bot_app.handlers.constants import CallbacksHandler

from loguru import logger

logger.add("error_logs.log", rotation="30 MB", backtrace=True, diagnose=True)

callback_router = Router()


@callback_router.callback_query(F.data == CallbacksHandler.BUTTON_MEETING)
async def callback_buttons(callback_query: types.CallbackQuery):
    """Callback message."""
    try:
        message = await callback_query.bot.send_message(
            chat_id=callback_query.from_user.id,
            text=CallbacksHandler.MESSAGE_CALLBACK
        )
        await bot.delete_message(
            chat_id=callback_query.from_user.id,
            message_id=callback_query.message.message_id
        )
        await asyncio.sleep(5)
        await callback_query.bot.delete_message(
            chat_id=callback_query.from_user.id,
            message_id=message.message_id
        )
    except Exception as e:
        await callback_query.bot.send_message(
            chat_id=callback_query.from_user.id,
            text=Messages.ERROR_MSG_FOR_USER
        )
        logger.error(f"Error in callback_buttons function: {e}")

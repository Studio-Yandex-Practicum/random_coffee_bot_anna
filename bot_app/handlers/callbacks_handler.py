import asyncio
from aiogram import F, Router, types
from bot_app.core.config import bot

from loguru import logger

logger.add("error_logs.log", rotation="500 MB", backtrace=True, diagnose=True)

MESSAGE_CALLBACK = 'Хорошо!'

callback_router = Router()


@callback_router.callback_query(F.data == 'button_meeting')
async def callback_buttons(callback_query: types.CallbackQuery):
    """Callback message."""
    try:
        message = await callback_query.bot.send_message(
            chat_id=callback_query.from_user.id,
            text=MESSAGE_CALLBACK
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
        logger.error(f"Error in callback_buttons function: {e}")

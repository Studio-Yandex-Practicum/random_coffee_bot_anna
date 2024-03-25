from aiogram import F, Router, types
from loguru import logger

logger.add("error_logs.log", level="ERROR")


MESSAGE_CALLBACK = 'Хорошо!'


callback_router = Router()


@callback_router.callback_query(F.data == 'button_meeting')
async def callback_buttons(callback_query: types.CallbackQuery):
    try:
        await callback_query.bot.send_message(
            chat_id=callback_query.from_user.id,
            text=MESSAGE_CALLBACK
        )
    except Exception as e:
        logger.error(f"Error in callback_buttons function: {e}")

import asyncio
from aiogram import F, Router, types
from bot_app.core.config import bot

MESSAGE_CALLBACK = 'Хорошо!'

callback_router = Router()


@callback_router.callback_query(F.data == 'button_meeting')
async def callback_buttons(callback_query: types.CallbackQuery):
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

from aiogram import F, Router, types


MESSAGE_CALLBACK = 'Хорошо!'


callback_router = Router()


@callback_router.callback_query(F.data == 'button_meeting')
async def callback_buttons(callback_query: types.CallbackQuery):
    await callback_query.bot.send_message(
        chat_id=callback_query.from_user.id,
        text=MESSAGE_CALLBACK
    )

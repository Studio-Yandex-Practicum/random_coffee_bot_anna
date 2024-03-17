from aiogram import types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.utils.i18n import gettext

from database.models import User
from enums.request import RequestEnum
from core.config import settings
from bot import dp
from filters.commands import CommandFilter
from keyboards.inline.request_kb import request_keyboard
from states.states import CommandsStates
from utils.answer import answer



@dp.message(Command("admin"), CommandFilter(CommandsStates.admin))
async def auth(message: types.Message, state: FSMContext, user: User):
    await state.set_state(CommandsStates.admin)
    await answer(
        chat_id=message.chat.id,
        text=gettext("messages.request.admin")
    )
    await answer(
        chat_id=settings.ADMIN_CHAT_ID,
        text=gettext("messages.command.admin").format(
            href=user.name
        ),
        reply_markup=request_keyboard(id=user.id,
                                        type_request=RequestEnum.ADMIN)
    )


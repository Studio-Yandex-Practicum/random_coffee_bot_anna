from typing import List, Tuple, Optional

from sqlalchemy.ext.asyncio import AsyncSession
from aiogram.types.inline_keyboard_markup import InlineKeyboardMarkup
from aiogram.types.inline_keyboard_button import InlineKeyboardButton

from bot_app.core.config import bot
from bot_app.database.models import User

MEETING_MESSAGE = '''
Ваша пара для Кофе вслепую {} {} ({}).
Договоритесь с коллегой о кофе брейке на этой неделе.
Приятного времяпровождения!
'''
MEET_OK = 'Встреча состоялась'
MEET_FALSE = 'Встреча не состоялась'
MEET_END_OF_WEEK = 'Встретимся в конце недели'
REMINDER_MAILING = 'Удалось ли уже встретиться с коллегой и выпить чашечку кофе?'

meet_inline_buttons = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text=MEET_OK, callback_data='button_meeting')],
        [InlineKeyboardButton(text=MEET_FALSE, callback_data='button_meeting')],
        [InlineKeyboardButton(text=MEET_END_OF_WEEK, callback_data='button_meeting')],
    ])


async def mailing_by_user_tg_id(chat_id: str,
                                text: str,
                                inline_buttons: Optional[InlineKeyboardMarkup] = None):
    await bot.send_message(chat_id=chat_id, text=text, reply_markup=inline_buttons)


async def meeting_mailing(meetings_pairs: List[Tuple[User, User]] = None):
    # test TODO: kill it
    from bot_app.database.engine import get_async_session
    sql_session = await anext(get_async_session())
    users = await User.get_all_activated(sql_session)
    meetings_pairs = [(users[0], users[0])]
    # // test

    for pair in meetings_pairs:
        await mailing_by_user_tg_id(chat_id=pair[0].tg_id,
                                    text=MEETING_MESSAGE.format(pair[1].name, pair[1].last_name, pair[1].email))
        await mailing_by_user_tg_id(chat_id=pair[1].tg_id,
                                    text=MEETING_MESSAGE.format(pair[0].name, pair[0].last_name, pair[0].email))


async def meeting_reminder_mailing(session: AsyncSession):
    users = await User.get_all_is_sent(session)
    for user in users:
        await mailing_by_user_tg_id(chat_id=user.tg_id, text=REMINDER_MAILING, inline_buttons=meet_inline_buttons)

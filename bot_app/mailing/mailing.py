from typing import List, Tuple, Optional

from sqlalchemy.ext.asyncio import AsyncSession
from aiogram.types.inline_keyboard_markup import InlineKeyboardMarkup
from aiogram.types.inline_keyboard_button import InlineKeyboardButton

from bot_app.core.config import bot
from bot_app.database.models import User
from bot_app.mailing.distribution import distribution

MEETING_MESSAGE = '''
Ваша пара для Кофе вслепую {} {} ({}).
Договоритесь с коллегой о кофе брейке на этой неделе.
Приятного времяпровождения!
'''
MEET_OK = 'Да'
MEET_FALSE = 'Нет'
MEET_END_OF_WEEK = 'Встретимся в конце недели'
REMINDER_MAILING = 'Удалось ли уже встретиться с коллегой и выпить чашечку кофе?'
TEXT_FOR_EXTRA = """
Привет!На этой неделе в нашем проекте «Кофе вслепую» нечетное количество
участников, поэтому имя коллеги тебе придет на следующей неделе.
Но сейчас не теряй возможность, пригласи на чашечку кофе любого
коллегу и предложи ему присоединиться к нашему проекту
(конечно, если он еще не участвует)!
Отличного дня и продуктивной недели😊
"""

meet_inline_buttons = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text=MEET_OK, callback_data='button_meeting'),
         InlineKeyboardButton(text=MEET_FALSE,
                              callback_data='button_meeting')],
        [InlineKeyboardButton(text=MEET_END_OF_WEEK,
                              callback_data='button_meeting')],
    ])


async def mailing_by_user_tg_id(chat_id: str,
                                text: str,
                                inline_buttons: Optional[InlineKeyboardMarkup] = None):
    await bot.send_message(chat_id=chat_id, text=text,
                           reply_markup=inline_buttons)


async def meeting_mailing(session: AsyncSession): #(meetings_pairs: List[Tuple[User, User]], no_pair):
    meetings_pairs, no_pair = await distribution(session)
    if no_pair:
        print(no_pair)
        await mailing_by_user_tg_id(chat_id=no_pair.tg_id, text=TEXT_FOR_EXTRA)
    print(meetings_pairs)
    for pair in meetings_pairs:
        await mailing_by_user_tg_id(chat_id=pair[0].tg_id,
                                    text=MEETING_MESSAGE.format(pair[1].name,
                                    pair[1].last_name, pair[1].email))
        await mailing_by_user_tg_id(chat_id=pair[1].tg_id,
                                    text=MEETING_MESSAGE.format(pair[0].name,
                                    pair[0].last_name, pair[0].email))


async def meeting_reminder_mailing(session: AsyncSession):
    users = await User.get_all_is_sent(session)
    await User.set_is_sent_status_false(users, session)
    for user in users:
        await mailing_by_user_tg_id(chat_id=user.tg_id,
                                    text=REMINDER_MAILING,
                                    inline_buttons=meet_inline_buttons)
